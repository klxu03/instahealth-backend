import os

from flask import Flask, request

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "instahealth.sqlite"),
    )

    os.makedirs(app.instance_path, exist_ok=True)

    from . import db
    db.init_app(app)

    @app.route("/")
    def root():
        return "<p>lol</p>"

    @app.route("/login")
    def login():
        return "login get"

    @app.route("/register")
    def register():
        return "register get"

    @app.route("/questions", methods=["GET", "POST"])
    def questions():
        if request.method == "GET":
            return "questions get"
        else:
            return "questions post"

    return app
