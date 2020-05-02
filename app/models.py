from app import db

# TODO: app_id needs to be explicitly indexed?
class App(db.Model):
    __tablename__ = 'APPS'

    achievements_enabled = db.Column(db.Boolean)
    app_id = db.Column(db.Unicode(20), index=True, primary_key=True)
    app_type = db.Column(db.UnicodeText)
    app_website = db.Column(db.UnicodeText)
    big_logo = db.Column(db.UnicodeText)
    captions = db.Column(db.Boolean)
    commentary = db.Column(db.Boolean)
    controller_support = db.Column(db.UnicodeText)
    hdr = db.Column(db.Boolean)
    hours_played = db.Column(db.Float)
    last_updated = db.Column(db.DateTime)
    leaderboards_enabled = db.Column(db.Boolean)
    metascore = db.Column(db.UnicodeText)
    metascore_link = db.Column(db.UnicodeText)
    minutes_played = db.Column(db.Integer)
    multiplayer = db.Column(db.Boolean)
    os_linux = db.Column(db.Boolean)
    os_mac = db.Column(db.Boolean)
    os_windows = db.Column(db.Boolean)
    release_date = db.Column(db.UnicodeText)
    required_age = db.Column(db.Integer)
    singleplayer = db.Column(db.Boolean)
    size_mb = db.Column(db.Float)
    source_sdk_included = db.Column(db.Boolean)
    stats_enabled = db.Column(db.Boolean)
    steamcloud_enabled = db.Column(db.Boolean)
    store_price_default_usd = db.Column(db.Float)
    tradingcards_enabled = db.Column(db.Boolean)
    VAC_enabled = db.Column(db.Boolean)
    workshop_enabled = db.Column(db.Boolean)

    def serialize(self):
        return {
            'achievements_enabled': self.achievements_enabled,
            'app_id': self.app_id,
            'app_type': self.app_type,
            'app_website': self.app_website,
            'big_logo': self.big_logo,
            'captions': self.captions,
            'commentary': self.commentary,
            'controller_support': self.controller_support,
            'hdr': self.hdr,
            'hours_played': self.hours_played,
            'last_updated': self.last_updated,
            'leaderboards_enabled': self.leaderboards_enabled,
            'metascore_link': self.metascore_link,
            'metascore': self.metascore,
            'minutes_played': self.minutes_played,
            'multiplayer': self.multiplayer,
            'os_linux': self.os_linux,
            'os_mac': self.os_mac,
            'os_windows': self.os_windows,
            'release_date': self.release_date,
            'required_age': self.required_age,
            'singleplayer': self.singleplayer,
            'size_mb': self.size_mb,
            'source_sdk_included': self.source_sdk_included,
            'stats_enabled': self.stats_enabled,
            'steamcloud_enabled': self.steamcloud_enabled,
            'store_price_default_usd': self.store_price_default_usd,
            'tradingcards_enabled': self.tradingcards_enabled,
            'VAC_enabled': self.VAC_enabled,
            'workshop_enabled': self.workshop_enabled
        }

    def __repr__(self):
        return '<App %s - "Name No Longer Stored" (%s%s) | Type: %s | Multi: %s | Price: $%s | Windows: %s | Mac: %s | Linux: %s | Joy: %s | Metacritic: %s | %s>' % (self.app_id, self.size_mb, ' MB', self.app_type, self.multiplayer, self.store_price_default_usd, self.os_windows, self.os_mac, self.os_linux, self.controller_support, self.metascore, self.big_logo)


class Time_To_Beat(db.Model):
    __tablename__ = 'TIME_TO_BEAT'

    app_id = db.Column(db.Unicode(20), index=True, primary_key=True)
    data_imputed_completionist = db.Column(db.Boolean)
    data_imputed_extras = db.Column(db.Boolean)
    data_imputed_main_game = db.Column(db.Boolean)
    hltb_id = db.Column(db.Unicode(20))
    minutes_to_beat_completionist = db.Column(db.Integer)
    minutes_to_beat_extras = db.Column(db.Integer)
    minutes_to_beat_main_game = db.Column(db.Integer)
    timetobeat_api_raw = db.Column(db.Text)

    def serialize(self):
        return {
            'data_imputed_completionist': self.data_imputed_completionist,
            'data_imputed_extras': self.data_imputed_extras,
            'data_imputed_main_game': self.data_imputed_main_game,
            'hltb_id': self.hltb_id,
            'minutes_to_beat_completionist': self.minutes_to_beat_completionist,
            'minutes_to_beat_extras': self.minutes_to_beat_extras,
            'minutes_to_beat_main_game': self.minutes_to_beat_main_game
        }


class Genre_App_Map(db.Model):
    __tablename__ = 'GENRE_APP_MAP'

    id = db.Column(db.Integer, index=True, primary_key=True, autoincrement=True)
    genres = db.Column(db.Unicode(200), index=True)
    apps = db.Column(db.Unicode(20), index=True)

    def serialize(self):
        return self.genres


class Developer_App_Map(db.Model):
    __tablename__ = 'DEVELOPER_APP_MAP'

    id = db.Column(db.Integer, index=True, primary_key=True, autoincrement=True)
    developers = db.Column(db.Unicode(200), index=True)
    apps = db.Column(db.Unicode(20), index=True)

    def serialize(self):
        return self.developers


class Publisher_App_Map(db.Model):
    __tablename__ = 'PUBLISHER_APP_MAP'

    id = db.Column(db.Integer, index=True, primary_key=True, autoincrement=True)
    publishers = db.Column(db.Unicode(200), index=True)
    apps = db.Column(db.Unicode(20), index=True)

    def serialize(self):
        return self.publishers


class Language_App_Map(db.Model):
    __tablename__ = 'LANGUAGE_APP_MAP'

    id = db.Column(db.Integer, index=True, primary_key=True, autoincrement=True)
    languages = db.Column(db.Unicode(200), index=True)
    apps = db.Column(db.Unicode(20), index=True)

    def serialize(self):
        return self.languages


class DLC_id_App_Map(db.Model):
    __tablename__ = 'DLC_ID_APP_MAP'

    id = db.Column(db.Integer, index=True, primary_key=True, autoincrement=True)
    dlc_ids = db.Column(db.Unicode(200), index=True)
    apps = db.Column(db.Unicode(20), index=True)


def littleBobby():
    db.drop_all()


def createAll():
    db.create_all()
