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

    def get_youtube_url(self, video_id):
        return "https://www.youtube.com/watch?v={video_id}".format(video_id=video_id)

    def get_stream_list(self, url):
        stream_list = []
        for stream in YouTube(url).streams.filter(progressive=True):
            stream_list.append({
                "itag": stream.itag,
                "mime_type": stream.mime_type,
                "res": stream.resolution,
                "fps": stream.fps,
                "vcodec": stream.video_codec,
                "acodec": stream.audio_codec,
                "progressive": stream.is_progressive,
                "type": stream.type
            })

        return stream_list

    # v: video_id
    # fps: 30fps, 60fps
    # res: 360p 480p, 720p 1080p
    # type: # video, audio
    def download(self, url, itag):
        yyyymmddhh = time.strftime('%Y%m%d%H')
        save_home = os.path.join(self.output_path, yyyymmddhh)
        if not os.path.exists(save_home):
            os.makedirs(save_home)

        media = YouTube(url).streams.get_by_itag(itag)
        if media is None:
            return {
                "status": "FAIL",
                "message": "Couldn't find the youtube media. Please check media spec."
                           " url: {url}, media_type: {media_type}, fps: {fps}, res: {res}".format(url=url,
                                                                                                  media_type=media.type,
                                                                                                  fps=media.fps,
                                                                                                  res=media.res),
                "error": "NOT_FOUND_EXCEPTION"
            }

        filename, file_extension = os.path.splitext(media.default_filename)
        filename = "{filename}_{media_type}_{fps}fps_{res}{file_extension}".format(filename=filename,
                                                                                   media_type=media.type,
                                                                                   fps=media.fps, res=media.resolution,
                                                                                   file_extension=file_extension)
        seq_filename, file_extension = self.get_seq_filename(save_home, filename)

        logging.info(
            "[Youtube Downloader] Start to download youtube media."
            ", filename: {seq_filename}"
            ", media_type: {media_type}, fps: {fps}, res: {res}"
            ", filesize: {filesize} MB".format(seq_filename=seq_filename
                                               , media_type=media.type, fps=media.fps, res=media.resolution
                                               , filesize=round(media.filesize / 1024 / 1024, 2)))

        saved_path = media.download(output_path=save_home, filename=seq_filename)

        logging.info(
            "[Youtube Downloader] Downloaded youtube media."
            ", filename: {seq_filename}"
            ", media_type: {media_type}, fps: {fps}, res: {res}"
            ", filesize: {filesize} MB".format(seq_filename=seq_filename
                                               , media_type=media.type, fps=media.fps, res=media.resolution
                                               , filesize=round(media.filesize / 1024 / 1024, 2)))

        return {
            "status": "SUCCESS",
            "youtube_url": url,
            "yyyymmddhh": yyyymmddhh,
            "filename": seq_filename + file_extension,
            "href": "/youtube/{yyyymmddhh}/{file}".format(yyyymmddhh=yyyymmddhh, file=seq_filename + file_extension),
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
