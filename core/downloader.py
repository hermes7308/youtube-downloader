# pip3 install pytube3
try:
    from pytube import YouTube
    from pytube import Playlist
except Exception as e:
    print("Some Modules are Missing {}".format(e))


class Downloader:
    def __init__(self, output_path=None):
        print("## Downloader created")
        self.output_path = output_path

    def download(self, v):
        url = "https://www.youtube.com/watch?v={video_id}".format(video_id=v)
        video = YouTube(url).streams.first()
        file_name = video.default_filename
        saved_path = video.download(self.output_path)

        return {
            "v": v,
            "file_name": file_name,
            "saved_path": saved_path
        }
