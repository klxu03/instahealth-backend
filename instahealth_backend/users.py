from flask import Blueprint, Response, request
from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db

bp = Blueprint('users', __name__)

ROLES = [
    "patient",
    "family-doctor",
    "cardiologist",
    "dermatologist",
    "optometrist",
    "dentist",
    "otolaryngologist",
]

@bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json(force=True)
        username = data["username"]
        password = data["password"]
        db = get_db()

        row = db.execute(
            "SELECT * FROM users WHERE username = ?",
            [username],
        ).fetchone()

        if row is None:
            raise ValueError("username is not registered")
        if not check_password_hash(user["password"], password):
            raise ValueError("password is incorrect")

    except Exception as e:
        return str(e), 400
    else:
        return "", 200

@bp.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json(force=True)
        username = data["username"]
        password = data["password"]
        role = data["role"]
        db = get_db()

        if not username:
            raise ValueError("username is required")
        if not password:
            raise ValueError("password is required")
        if role not in ROLES:
            raise ValueError(f"role not in {', '.join(ROLES)}")
        if db.execute(
            "SELECT id FROM users WHERE username = ?",
            [username],
        ).fetchone() is not None:
            raise ValueError("username already registered")

        db.execute(
            (
                "INSERT INTO users (username, password, role)"
                " VALUES (?, ?, ?)"
            ),
            [username, generate_password_hash(password), role],
        )
        db.commit()

    except Exception as e:
        return repr(e), 400
    else:
        return "", 200
