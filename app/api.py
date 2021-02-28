import os, requests
from flask import jsonify
import app.models as models


API_KEY = os.getenv('API_KEY')


def get_id_by_username(username):
    request = {
        'protocol': 'https://',
        'host': 'api.steampowered.com',
        'path': '/ISteamUser/ResolveVanityURL/v1',
        'payload': {'vanityurl': username}
    }
    account_id = make_request(request, True)

    return account_id


def get_account_summary(account_id):
    # TODO: this endpoint can handle up to 100 (comma-delimited) ids (per api documentation). larger lists will need to be broken into separate requests.
    request = {
        'protocol': 'https://',
        'host': 'api.steampowered.com',
        'path': '/ISteamUser/GetPlayerSummaries/v2',
        'payload': {'steamids': account_id}
    }
    accounts = make_request(request, True)

    return accounts


def get_friend_list(account_id):
    request = {
        'protocol': 'https://',
        'host': 'api.steampowered.com',
        'path': '/ISteamUser/GetFriendList/v1',
        'payload': {'relationship': 'friend', 'steamid': account_id}
    }
    user_friends = make_request(request, True)

    return user_friends


def get_owned_games(account_id):
    request = {
        'protocol': 'https://',
        'host': 'api.steampowered.com',
        'path': '/IPlayerService/GetOwnedGames/v1',
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


def get_app_details(app_ids, fields):
    include_fields = []

    if fields:
        include_fields = fields.split(',')

    rows = models.db.session.query(models.App).filter(models.App.app_id.in_(str(app_ids).split(',')))

    if rows:
        app_list = []

        for row in rows:
            app_data = row.serialize()

            if 'time_to_beat' in include_fields:
                if row.time_to_beat:
                    app_data.update({'time_to_beat': row.time_to_beat.serialize()})
                else:
                    app_data.update({'time_to_beat': None})

            if 'developers' in include_fields:
                developers = [developer.serialize() for developer in row.developers]
                app_data.update({'developers': developers})

            if 'genres' in include_fields:
                genres = [genre.serialize() for genre in row.genres]
                app_data.update({'genres': genres})

            if 'languages' in include_fields:
                languages = [language.serialize() for language in row.languages]
                app_data.update({'languages': languages})

            if 'publishers' in include_fields:
                publishers = [publisher.serialize() for publisher in row.publishers]
                app_data.update({'publishers': publishers})

            app_list.append(app_data)

        return app_list

    return None


def format_query(query):
    if not query:
        return jsonify({'meta': {'success': False}, 'data': None})

    return jsonify({'meta': {'success': True}, 'data': query})


def make_request(request, requires_api_key):
    if requires_api_key:
        request['payload']['key'] = API_KEY

    # TODO refactor to pattern: {protocol}://{host}/{interface}/{method}/{version}?{parameters}
    request_url = '%(protocol)s%(host)s%(path)s' % request

    # response is formatted as json by default. vdf and xml is also available via the "format" param
    # TODO: add timeout to requests- http://docs.python-requests.org/en/master/user/quickstart/#timeouts
    response = requests.get(request_url, params=request['payload'])

    if response.status_code != 200:
        raise ResourceError('The response returned status code of [' + str(response.status_code) + ']')

    response_parsed = response.json()

    # collapse top tree level if top key is named "response"
    if 'response' in response_parsed.keys():
        response_parsed = response_parsed.get('response')

    # The request was successful, but the response shape returned indicates
    # an issue with (maybe?) permissions and/or the API key.
    # Reminder: empty dict and list are each falsy
    if type(response_parsed) is dict and not response_parsed:
        raise ResourceDataError('The response returned an empty object.')

    return response_parsed

class ResourceError(LookupError):
    '''The external resource response status code was not 200'''

class ResourceDataError(ValueError):
    '''The request was successful, but the response shape returned was malformed or unexpected.'''
