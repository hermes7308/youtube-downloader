import logging


class Config(object):
    # Common
    HOST = "0.0.0.0"
    PORT = 5005
    LOG_FILENAME = "youtube_download_output.log"

    # Priority
    LOG_LEVEL = logging.INFO
    LOG_HOME = "/home/irteam/logs/"
    HOME_PATH = "/home/irteam/data/youtube"


class ReleaseConfig(Config):
    LOG_LEVEL = logging.INFO
    HOME_PATH = "/home/irteam/data/youtube"


class DevelopConfig(Config):
    LOG_LEVEL = logging.INFO
    HOME_PATH = "/home/irteam/data/youtube"


class LocalConfig(Config):
    LOG_LEVEL = logging.DEBUG
    LOG_HOME = "C:\\youtubedownloader\\logs\\"
    HOME_PATH = "C:\\youtubedownloader\\data\\youtube"
