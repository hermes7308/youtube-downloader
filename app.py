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


@app.route("/download", methods=["GET"])
def download():
    global result
    v = request.args.get("v")
    if v is None:
        return {
            "status": "FAIL",
            "message": "Url is empty."
        }

    try:
        result = downloader.download(v)
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
    app.run(host='0.0.0.0', port=5003)
