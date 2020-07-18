import atexit
import logging
import os

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template, request, send_from_directory

from core.downloader import Downloader
from core.remover import Remover

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

home_path = "C:\\Users\\herme\\Desktop\\video\\youtube"

downloader = Downloader(home_path)
remover = Remover(home_path)


def remove_video_job():
    remover.remove()


scheduler = BackgroundScheduler()
scheduler.add_job(func=remove_video_job, trigger="interval", seconds=3600)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get-support-spec")
def get_support_spec():
    v = request.args.get("v")
    if v is None:
        return {
            "status": "FAIL",
            "message": "Url is empty."
        }

    url = downloader.get_youtube_url(video_id=v)
    type_list, fps_list, res_list = downloader.get_support_spec(url)
    return {
        "status": "SUCCESS",
        "type_list": type_list,
        "fps_list": fps_list,
        "res_list": res_list
    }


@app.route("/download", methods=["GET"])
def download():
    global result
    v = request.args.get("v")
    if v is None:
        return {
            "status": "FAIL",
            "message": "Url is empty."
        }
    media_type = request.args.get("media_type")
    fps = request.args.get("fps")
    res = request.args.get("res")

    try:
        result = downloader.download(v=v, fps=fps, res=res, media_type=media_type)
        return result
    except Exception as e:
        logging.error(e)
        return {
            "status": "FAIL",
            "message": "Couldn't download this video",
            "error": str(e)
        }


@app.route("/download-video", methods=["GET"])
def download_video():
    yyyymmdd = request.args.get("yyyymmdd")
    filename = request.args.get("filename")
    directory = os.path.join(home_path, yyyymmdd)

    return send_from_directory(directory, filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)
