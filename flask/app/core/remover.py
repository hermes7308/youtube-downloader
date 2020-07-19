import logging
import os
from datetime import datetime, timedelta


class Remover:
    def __init__(self, home_path=None):
        self.home_path = home_path

    def remove(self):
        yyyymmddhh = (datetime.now() - timedelta(hours=1)).strftime('%Y%m%d%H')

        for directory in os.listdir(self.home_path):
            # Delete past directory
            if directory < yyyymmddhh:
                directory_path = os.path.join(self.home_path, directory)

                logging.info(
                    "[Youtube Downloader] Start remove directory."
                    " directory_path:  {directory_path}".format(directory_path=directory_path))

                for filename in os.listdir(directory_path):
                    filepath = os.path.join(directory_path, filename)
                    if os.path.isfile(filepath):
                        os.remove(filepath)
                        logging.info(
                            "[Youtube Downloader] Removed a file."
                            " filepath:  {filepath}".format(filepath=filepath))

                os.rmdir(directory_path)

                logging.info(
                    "[Youtube Downloader] Removed directory."
                    " directory_path:  {directory_path}".format(directory_path=directory_path))
