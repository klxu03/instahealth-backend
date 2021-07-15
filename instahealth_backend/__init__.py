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

    from . import users
    app.register_blueprint(users.bp)

    from . import questions
    app.register_blueprint(questions.bp)

    from . import cors
    cors.cors.init_app(app)

    @app.route("/")
    def root():
        return "<p>lol</p>"

    return app
