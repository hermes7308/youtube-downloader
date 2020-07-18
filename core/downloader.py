import logging
import os
import time

try:
    from pytube import YouTube
    from pytube import Playlist
except Exception as e:
    logging.error("Some Modules are Missing {}".format(e))


class Downloader:
    def __init__(self, output_path=None):
        self.output_path = output_path

    def download(self, v):
        yyyymmdd = time.strftime('%Y%m%d')
        save_home = os.path.join(self.output_path, yyyymmdd)
        if not os.path.exists(save_home):
            os.makedirs(save_home)

        url = "https://www.youtube.com/watch?v={video_id}".format(video_id=v)
        video = YouTube(url).streams.first()
        seq_filename, file_extension = self.get_seq_filename(save_home, video.default_filename)

        logging.info(
            "[Youtube Downloader] Start youtube download."
            " default_filename:  {default_filename}"
            ", seq_filename: {seq_filename}"
            ", filesize: {filesize} MB".format(default_filename=video.default_filename
                                               , seq_filename=seq_filename
                                               , filesize=round(video.filesize / 1024 / 1024, 2)))

        saved_path = video.download(output_path=save_home, filename=seq_filename)

        logging.info("[Youtube Downloader] Saved the video."
                     " default_filename:  {default_filename}"
                     ", seq_filename: {seq_filename}"
                     ", filesize: {filesize} MB".format(default_filename=video.default_filename
                                                        , seq_filename=seq_filename
                                                        , filesize=round(video.filesize / 1024 / 1024, 2)))

        return {
            "status": "SUCCESS",
            "v": v,
            "yyyymmdd": yyyymmdd,
            "filename": seq_filename + file_extension,
            "saved_path": saved_path
        }

    @staticmethod
    def get_seq_filename(home=None, default_filename=None):
        filename, file_extension = os.path.splitext(default_filename)
        new_filename = filename

        seq = 0
        while True:
            new_file_path = os.path.join(home, new_filename + file_extension)

            if os.path.exists(new_file_path):
                seq += 1
                new_filename = (filename + " (%s)") % seq
                continue
            else:
                return new_filename, file_extension
