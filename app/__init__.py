import os
from datetime import datetime, timezone
from flask import Flask, abort, jsonify, session, redirect, request
from flask_sqlalchemy import SQLAlchemy

flaskApp = Flask(__name__)
flaskApp.config.update(
    SQLALCHEMY_DATABASE_URI=os.getenv('SQLALCHEMY_DATABASE_URI'),
    SQLALCHEMY_TRACK_MODIFICATIONS=os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS'),
    SECRET_KEY=os.getenv('SECRET_KEY')
)
ADMIN_USERS = os.getenv('ADMIN_USERS').split(',')
DEBUG_MODE = os.getenv('DEBUG')
REACT_DOMAIN = os.getenv('REACT_JS_DOMAIN')
MINUTES_EXPIRE = int(os.getenv('SESSION_EXPIRE_MINUTES'))
REACT_JS_PORT = os.getenv('REACT_JS_PORT')

db = SQLAlchemy(flaskApp)

# must be imported after creation of db object
import app.api as api

if DEBUG_MODE:
    REACT_DOMAIN += ':'+REACT_JS_PORT


@flaskApp.before_request
def before_request():
    if session and session['account_id'] and session['last_action']:
        # If more than x minutes have passed since the last time the user did anything, log them out
        if (datetime.now(timezone.utc) - session['last_action']).seconds > (MINUTES_EXPIRE*60):
            clear_session()
        else:
            # check anything that might have changed
            if session['account_id'] in ADMIN_USERS:
                session['admin']=True
            else:
                session['admin']=False
            session['last_action'] = datetime.now(timezone.utc)
    else:
        clear_session()


@flaskApp.route('/authorize', methods=['GET'])
def authorize():
    response = request.args['openid.identity']
    session['account_id'] = response.split('/')[-1].strip('"')

    dateTimeNow = datetime.now(timezone.utc)
    session['session_start'] = dateTimeNow
    session['last_action'] = dateTimeNow

    if session['account_id'] in ADMIN_USERS:
        session['admin'] = True

    return redirect(REACT_DOMAIN)


@flaskApp.route('/current_user')
def current_user():
    response = {
        'account_id': session['account_id'],
        'admin': session['admin'],
        'last_action': session['last_action'],
        'session_start': session['session_start']
    }

    return jsonify(response)


@flaskApp.route('/logout', methods=['PUT'])
def logout():
    clear_session()
    response = {
        'account_id': session['account_id'],
        'admin': session['admin'],
        'last_action': session['last_action'],
        'session_start': session['session_start']
    }

    return jsonify(response)


@flaskApp.route('/api/1.0/apps', methods=['GET'])
def get_app_list():
    filter_multiplayer = request.args.get('filter_multiplayer', '', type=str) == 'true'

    if filter_multiplayer:
        response = api.get_multiplayer_app_list()
        return api.format_query(response)

    response = api.get_full_app_list()

    return api.format_query(response)


@flaskApp.route('/api/1.0/username/<string:username>', methods=['GET'])
def get_account_id(username):
    if len(username) > 0:
        response = api.get_id_by_username(username)

        return api.format_query(response)
    abort(404)


@flaskApp.route('/api/1.0/accounts/<string:account_id>', methods=['GET'])
def get_account_summary(account_id):
    # Note: account_id is a string to accommodate comma-delimited ids
    response = api.get_account_summary(account_id)

    return api.format_query(response)


@flaskApp.route('/api/1.0/accounts/<int:account_id>/apps', methods=['GET'])
def get_account_games(account_id):
    response = api.get_owned_games(account_id)
    include_fields = request.args.get('fields')

    if response['game_count'] and include_fields:
        app_list = response['games']
        app_ids = ''
        for index, app in enumerate(app_list):
            if index != 0:
                app_ids += ','
            app_ids += str(app['appid'])

        app_details_list = api.get_app_details(app_ids, include_fields)

        return api.format_query(app_details_list)

    return api.format_query(response['games'])


@flaskApp.route('/api/1.0/accounts/<int:account_id>/friends', methods=['GET'])
def get_friends(account_id):
    response = api.get_friend_list(account_id)

    return api.format_query(response)


@flaskApp.errorhandler(404)
def not_found(error):
    return jsonify({
        'meta': {
            'code': 404,
            'error_key': 'not_found',
            'error': str(error),
            'success': False
        },
    }), 404


@flaskApp.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        'meta': {
            'code': 500,
            'error_key': 'SERVER_ISSUE',
            'error': str(error),
            'success': False
        },
    }), 500


@flaskApp.errorhandler(api.ResourceError)
def resource_error(error):
    return jsonify({
        'meta': {
            'code': 500,
            'error_key': 'COULD_NOT_GET_EXTERNAL_DATA',
            'error': str(error),
            'success': False
        },
    }), 503


@flaskApp.errorhandler(api.ResourceDataError)
def resource_data_error(error):
    return jsonify({
        'meta': {
            'code': 500,
            'error_key': 'BAD_DATA_RETURNED',
            'error': str(error),
            'success': False
        },
    }), 500


def clear_session():
    session['account_id'] = None
    session['admin'] = False
    session['last_action'] = None
    session['session_start'] = None


if __name__ == '__main__':
    flaskApp.run(threaded=True, host='0.0.0.0')
