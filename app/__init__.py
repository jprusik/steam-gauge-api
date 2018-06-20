from flask import Flask, abort, jsonify
from flask_sqlalchemy import SQLAlchemy

flaskApp = Flask(__name__)
flaskApp.config.from_object('app.config')

db = SQLAlchemy(flaskApp)

# must be imported after creation of db object
import app.api as api

@flaskApp.route('/api/1.0/apps', methods=['GET'])
def get_app_list():
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


if __name__ == '__main__':
    flaskApp.run(threaded=True)
