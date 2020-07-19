from flask import Flask

app = Flask(__name__)
app.config.from_object("config.LocalConfig")

if app.config["ENV"] == "release":
    app.config.from_object("config.ReleaseConfig")
elif app.config["ENV"] == "dev":
    app.config.from_object("config.DevelopConfig")
else:
    app.config.from_object("config.LocalConfig")

from flask.app import views
