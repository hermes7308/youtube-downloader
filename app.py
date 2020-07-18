from flask import Flask, render_template, request, send_file

from core.downloader import Downloader

# save_path = "C:\\Users\\herme\\Desktop\\video\\youtube"
# downloader = Downloader(save_path)
# url = "https://www.youtube.com/watch?v=0qSEWvvA6gU"
# downloader.download(url)

downloader = Downloader()
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/download", methods=["GET"])
def download():
    v = request.args.get("v")
    if v is None:
        return {
            "status": "FAIL",
            "message": "Url is empty."
        }

    try:
        result = downloader.download(v)
        result["status"] = "SUCCESS"
        return result
    except Exception as e:
        print(e)
        return {
            "status": "FAIL",
            "message": "Couldn't download result: " + result
        }


@app.route("/download-video", methods=["GET"])
def download_video():
    file_name = request.args.get("file_name")
    return send_file(file_name)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
