from flask import Blueprint

from .db import get_db

bp = Blueprint('users', __name__)

@bp.route("/login")
def login():
    db = get_db()
    return "login get"

@bp.route("/register")
def register():
    db = get_db()
    return "register get"
