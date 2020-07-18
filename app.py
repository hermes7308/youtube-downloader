import logging
import os

from flask import Flask, render_template, request, send_from_directory

from core.downloader import Downloader

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

output_path = "C:\\Users\\herme\\Desktop\\video\\youtube"
downloader = Downloader(output_path)


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
    directory = os.path.join(output_path, yyyymmdd)

    return send_from_directory(directory, filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
