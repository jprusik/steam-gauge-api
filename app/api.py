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


def get_multiplayer_app_list():
    query = models.App.query.filter(models.App.multiplayer != None).values(models.App.app_id)
    app_data = [{'appid': int(x._asdict()['app_id'])} for x in query]

    return {'applist': {'apps': app_data}}


def get_app_details(app_id, fields):
    include_fields = []

    if fields:
        include_fields = fields.split(',')

    query = models.App.query.filter_by(app_id=str(app_id)).first()

    if query:
        app_data = query.serialize()

        if 'developers' in include_fields:
            developers_data = get_app_developers(app_id)
            app_data.update({'developers': developers_data})

        if 'genres' in include_fields:
            genres_data = get_app_genres(app_id)
            app_data.update({'genres': genres_data})

        if 'languages' in include_fields:
            languages_data = get_app_languages(app_id)
            app_data.update({'languages': languages_data})

        if 'publishers' in include_fields:
            publishers_data = get_app_publishers(app_id)
            app_data.update({'publishers': publishers_data})

        if 'time_to_beat' in include_fields:
            time_to_beat_data = get_time_to_beat(app_id)
            app_data.update({'time_to_beat': time_to_beat_data})

        return app_data

    return None


def get_time_to_beat(app_id):
    query = models.Time_To_Beat.query.filter_by(app_id=str(app_id)).first()

    if not query:
        return None

    return query.serialize()


def get_app_genres(app_id):
    query = models.Genre_App_Map.query.filter_by(apps=str(app_id)).all()

    if not query:
        return []

    return [ genre.serialize() for genre in query ]


def get_app_developers(app_id):
    query = models.Developer_App_Map.query.filter_by(apps=str(app_id)).all()

    if not query:
        return []

    return [ developer.serialize() for developer in query ]


def get_app_publishers(app_id):
    query = models.Publisher_App_Map.query.filter_by(apps=str(app_id)).all()

    if not query:
        return []

    return [ publisher.serialize() for publisher in query ]


def get_app_languages(app_id):
    query = models.Language_App_Map.query.filter_by(apps=str(app_id)).all()

    if not query:
        return []

    return [ language.serialize() for language in query ]


def format_query(query):
    if not query:
        return jsonify(success=False, data=None)

    return jsonify(success=True, data=query)


def make_request(request, requires_api_key):
    if requires_api_key:
        # TODO: load this from app.config instead of importing again?
        request['payload']['key'] = config.API_KEY

    # TODO refactor to pattern: {protocol}://{host}/{interface}/{method}/{version}?{parameters}
    request_url = '%(protocol)s%(host)s%(path)s' % request

    # response is formatted as json by default. vdf and xml is also available via the "format" param
    # TODO: add timeout to requests- http://docs.python-requests.org/en/master/user/quickstart/#timeouts
    response = requests.get(request_url, params=request['payload'])

    # TODO: Handle request exceptions
    if response.status_code != 200:
        return jsonify(success=False, data=None)

    # collapse top tree level if top key is named "response"
    response_parsed = response.json().get('response') or response.json()

    return response_parsed
