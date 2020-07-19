import logging.config
import os

import coloredlogs
import yaml

from app import app


def setup_logging(default_path='logging.yaml', default_level=logging.INFO, env_key='LOG_CFG', filename="output.log"):
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            try:
                config = yaml.safe_load(f.read())
                config["handlers"]["file"]["filename"] = filename
                logging.config.dictConfig(config)
                coloredlogs.install()
            except Exception as e:
                print(e)
                print('Error in Logging Configuration. Using default configs')
                logging.basicConfig(level=default_level)
                coloredlogs.install(level=default_level)
    else:
        logging.basicConfig(level=default_level)
        coloredlogs.install(level=default_level)
        print('Failed to load configuration file. Using default configs')


if __name__ == "__main__":
    # Setup log
    log_file = os.path.join(app.config["LOG_HOME"], app.config["LOG_FILENAME"])
    setup_logging(default_level=app.config["LOG_LEVEL"], filename=log_file)

    app.run(host=app.config["HOST"], port=app.config["PORT"])
