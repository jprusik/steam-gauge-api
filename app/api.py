import requests
from flask import jsonify

import app.models as models
import app.mocks as mocks
import app.config as config


def get_id_by_username(username):
    request = {
        'protocol': 'https://',
        'host': 'api.steampowered.com',
        'path': '/ISteamUser/ResolveVanityURL/v0001',
        'payload': {'vanityurl': username}
    }
    account_id = make_request(request, True)

    return account_id

def get_account_summary(account_id):
    # TODO: this endpoint can handle up to 100 (comma-delimited) ids (per api documentation). larger lists will need to be broken into separate requests.
    request = {
        'protocol': 'https://',
        'host': 'api.steampowered.com',
        'path': '/ISteamUser/GetPlayerSummaries/v0002',
        'payload': {'steamids': account_id}
    }
    accounts = make_request(request, True)

    return accounts


def get_friend_list(account_id):
    request = {
        'protocol': 'https://',
        'host': 'api.steampowered.com',
        'path': '/ISteamUser/GetFriendList/v0001',
        'payload': {'relationship': 'friend', 'steamid': account_id}
    }
    user_friends = make_request(request, True)

    return user_friends


def get_owned_games(account_id):
    request = {
        'protocol': 'https://',
        'host': 'api.steampowered.com',
        'path': '/IPlayerService/GetOwnedGames/v0001',
        'payload': {'include_played_free_games': 1, 'include_appinfo': 1, 'steamid': account_id}
    }
    user_games = make_request(request, True)

    return user_games


def get_full_app_list():
    request = {
        'protocol': 'https://',
        'host': 'api.steampowered.com',
        'path': '/ISteamApps/GetAppList/v2',
        'payload': {}
    }
    apps = make_request(request, False)

    return apps


def get_app_details(app_id):
    query = models.App.query.filter_by(app_id=str(app_id)).first()

    if query:
        app_data = query.__dict__
        del app_data['_sa_instance_state']

        return format_query(app_data)

    return format_query(None)


def get_time_to_beat(app_id):
    query = models.Time_To_Beat.query.filter_by(app_id=str(app_id)).first()

    if query:
        app_data = query.__dict__
        del app_data['_sa_instance_state']
        del app_data['timetobeat_api_raw']
        del app_data['app_id']

        return format_query(app_data)

    return format_query(None)


def get_app_genres(app_id):
    query = models.Genre_App_Map.query.filter_by(apps=str(app_id)).all()
    genres = []

    for g in query:
        genres.append(g.genres)

    return format_query(genres)


def get_app_developers(app_id):
    query = models.Developer_App_Map.query.filter_by(apps=str(app_id)).all()
    developers = []

    for d in query:
        developers.append(d.developers)

    return format_query(developers)


def get_app_publishers(app_id):
    query = models.Publisher_App_Map.query.filter_by(apps=str(app_id)).all()
    publishers = []

    for p in query:
        publishers.append(p.publishers)

    return format_query(publishers)


def get_app_languages(app_id):
    query = models.Language_App_Map.query.filter_by(apps=str(app_id)).all()
    languages = []

    for l in query:
        languages.append(l.languages)

    return format_query(languages)


# def sanitize_input(input):
#     return input


def format_query(query):
#     # handle db errors and return helpful response
    return jsonify({'success': True, 'data': query})


def make_request(request, requires_api_key):
    if requires_api_key:
        # TODO: load this from app.config instead of importing again?
        request['payload']['key'] = config.API_KEY

    # TODO refactor to pattern: {protocol}://{host}/{interface}/{method}/{version}?{parameters}
    request_url = '%(protocol)s%(host)s%(path)s' % request

    # response is formatted as json by default. vdf and xml is also available via the "format" param
    # TODO: add timeout to requests- http://docs.python-requests.org/en/master/user/quickstart/#timeouts
    response = requests.get(request_url, params=request['payload'])

    # TODO: Handle request exceptions- http://docs.python-requests.org/en/master/user/quickstart/#errors-and-exceptions
    if response.status_code != 200:
        return jsonify({'success': False, 'data': None})

    # collapse top tree level if top key is named "response"
    response_parsed = response.json().get('response') or response.json()

    return jsonify({'success': True, 'data': response_parsed})
