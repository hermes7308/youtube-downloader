import logging


class Config(object):
    LOGGING_LEVEL = logging.INFO

    HOME_PATH = "/home/irteam/data/youtube"


class ReleaseConfig(Config):
    pass


class DevelopConfig(Config):
    pass


class LocalConfig(Config):
    LOGGING_LEVEL = logging.DEBUG

    HOME_PATH = "C:\\youtubedownloader\\data\\youtube"
