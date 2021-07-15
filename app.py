from flask import Flask

app = Flask(__name__)

@app.route("/")
def root():
    return "<p>lol</p>"

@app.route("/login")
def login():
    return "hahasike"
