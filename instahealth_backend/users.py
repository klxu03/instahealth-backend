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
        email = data["email"]
        password = data["password"]
        db = get_db()

        row = db.execute(
            "SELECT * FROM users WHERE email = ?",
            [email],
        ).fetchone()

        if row is None:
            raise ValueError("email is not registered")
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
        email = data["email"]
        password = data["password"]
        role = data["role"]
        db = get_db()

        if not email:
            raise ValueError("email is required")
        if not password:
            raise ValueError("password is required")
        if role not in ROLES:
            raise ValueError(f"role not in {', '.join(ROLES)}")
        if db.execute(
            "SELECT id FROM users WHERE email = ?",
            [email],
        ).fetchone() is not None:
            raise ValueError("email already registered")

        db.execute(
            (
                "INSERT INTO users (email, password, role)"
                " VALUES (?, ?, ?)"
            ),
            [email, generate_password_hash(password), role],
        )
        db.commit()

    except Exception as e:
        return repr(e), 400
    else:
        return "", 200

@bp.route("/account/<int:account_id>", methods=["GET"])
def account_exists(account_id):
    try:
        db = get_db()

        if db.execute(
            "SELECT id FROM users WHERE id = ?",
            [account_id],
        ).fetchone() is not None:
            raise ValueError("Account does not exist")

    except Exception as e:
        return repr(e), 400
    else:
        return {"id": account_id}, 200
