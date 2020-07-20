import atexit
import logging

from app import app
from app.core.downloader import Downloader
from app.core.remover import Remover
from apscheduler.schedulers.background import BackgroundScheduler
from flask import render_template, request

downloader = Downloader(app.config["HOME_PATH"])
remover = Remover(app.config["HOME_PATH"])


def remove_video_job():
    remover.remove()


scheduler = BackgroundScheduler()
scheduler.add_job(func=remove_video_job, trigger="interval", seconds=600)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get-stream-list")
def get_stream_list():
    v = request.args.get("v")
    if v is None:
        return {
            "status": "FAIL",
            "message": "Url is empty."
        }

    url = downloader.get_youtube_url(video_id=v)
    try:
        stream_list = downloader.get_stream_list(url)
        return {
            "status": "SUCCESS",
            "stream_list": stream_list,
        }
    except Exception as e:
        logging.error("This is block download. exception: {e}".format(e=e))
        return {
            "status": "FAIL",
            "message": "Sorry, this youtube is block to download."
        }


@app.route("/download", methods=["GET"])
def download():
    v = request.args.get("v")
    if v is None:
        return {
            "status": "FAIL",
            "message": "Url is empty."
        }
    media_type = request.args.get("media_type")
    mime_type = request.args.get("mime_type")
    fps = int(request.args.get("fps"))
    res = request.args.get("res")

    try:
        return downloader.download(v=v, media_type=media_type, mime_type=mime_type, fps=fps, res=res)
    except Exception as e:
        logging.error(e)
        return {
            "status": "FAIL",
            "message": "Couldn't download this video",
            "error": str(e)
        }
