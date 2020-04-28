import datetime
from flask import Flask, abort, jsonify, session, redirect, request
from flask_sqlalchemy import SQLAlchemy

flaskApp = Flask(__name__)
flaskApp.config.from_object('app.config')

db = SQLAlchemy(flaskApp)

# must be imported after creation of db object
import app.api as api


react_domain = config.REACT_JS_DOMAIN
if config.DEBUG:
    react_domain += ':'+config.REACT_JS_PORT

@flaskApp.before_request
def before_request():
    if session and session['account_id']:
        # If more than x minutes have passed since the last time the user did anything, log them out
        minutes_expire = config.SESSION_EXPIRE_MINUTES
        if (datetime.datetime.now()-session['last_action']).seconds > (minutes_expire*60):
            clear_session()
        else:
            # check anything that might have changed
            if session['account_id'] in config.ADMIN_USERS:
                session['admin']=True
            else:
                session['admin']=False
            session['last_action'] = datetime.datetime.now()
    else:
        clear_session()


@flaskApp.route('/authorize', methods=['GET'])
def authorize():
    response = request.args['openid.identity']
    session['account_id'] = response.split('/')[-1].strip('"')
    session['session_start'] = datetime.datetime.now()
    session['last_action'] = datetime.datetime.now()
    if session['account_id'] in config.ADMIN_USERS:
        session['admin'] = True
    return redirect(react_domain)


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
        return response

    response = api.get_full_app_list()
    return response


@flaskApp.route('/api/1.0/apps/<int:app_id>', methods=['GET'])
def get_app(app_id):
    response = api.get_app_details(app_id)
    return response


@flaskApp.route('/api/1.0/apps/<int:app_id>/timeToBeat', methods=['GET'])
def get_time_to_beat(app_id):
    response = api.get_time_to_beat(app_id)
    return response


@flaskApp.route('/api/1.0/apps/<int:app_id>/genres', methods=['GET'])
def get_genres(app_id):
    response = api.get_app_genres(app_id)
    return response


@flaskApp.route('/api/1.0/apps/<int:app_id>/developers', methods=['GET'])
def get_developers(app_id):
    response = api.get_app_developers(app_id)
    return response


@flaskApp.route('/api/1.0/apps/<int:app_id>/publishers', methods=['GET'])
def get_publishers(app_id):
    response = api.get_app_publishers(app_id)
    return response


@flaskApp.route('/api/1.0/apps/<int:app_id>/languages', methods=['GET'])
def get_languages(app_id):
    response = api.get_app_languages(app_id)
    return response


@flaskApp.route('/api/1.0/username/<string:username>', methods=['GET'])
def get_account_id(username):
    if len(username) > 0:
        response = api.get_id_by_username(username)
        return response
    abort(404)


@flaskApp.route('/api/1.0/accounts/<string:account_id>', methods=['GET'])
def get_account_summary(account_id):
    # Note: account_id is a string to accommodate comma-delimited ids
    response = api.get_account_summary(account_id)
    return response


@flaskApp.route('/api/1.0/accounts/<int:account_id>/apps', methods=['GET'])
def get_account_games(account_id):
    response = api.get_owned_games(account_id)
    return response


@flaskApp.route('/api/1.0/accounts/<int:account_id>/friends', methods=['GET'])
def get_friends(account_id):
    response = api.get_friend_list(account_id)
    return response


@flaskApp.errorhandler(404)
def not_found(error):
    return jsonify({'success': False})


def clear_session():
    session['account_id'] = None
    session['admin'] = False
    session['last_action'] = None
    session['session_start'] = None


if __name__ == '__main__':
    flaskApp.run(threaded=True)
