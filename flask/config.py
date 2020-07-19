import logging


class Config(object):
    LOGGING_LEVEL = logging.INFO

    HOME_PATH = "/home/irteam/data/youtube"


class ReleaseConfig(Config):

    HOME_PATH = "/home/irteam/data/youtube"


class DevelopConfig(Config):

    HOME_PATH = "/home/irteam/data/youtube"


class LocalConfig(Config):
    LOGGING_LEVEL = logging.DEBUG

    HOME_PATH = "C:\\youtubedownloader\\data\\youtube"
