import re

from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db
from .assoc import get_assoc_dict
from .email import send_email

bp = Blueprint("questions", __name__)

def format_question(row):
    db = get_db()

    data = {
        key: row[key]
        for key in [
            "id",
            "question",
            "content",
            "authorName",
            "datePosted",
        ]
    }
    data["categories"] = row["categories"].split()

    question_id = data["id"]
    data["answers"] = [
        format_answer(row)
        for row in db.execute(
            "SELECT * FROM answers WHERE questionId = ?",
            [question_id],
        ).fetchall()
    ]

    return data

def format_answer(row):
    return {
        key: row[key]
        for key in [
            "id",
            "questionId",
            "content",
            "authorName",
            "role",
            "datePosted",
        ]
    }

category_to_role = {
    "general": "familyDoctor",
    "heart": "cardiologist",
    "skin": "dermatologist",
    "eye": "optometrist",
    "teeth": "dentist",
    "ear": "otolaryngologist",
}

def _add_question(data):
    db = get_db()
    question = data["question"]
    content = data["content"]
    author_name = data["authorName"]

    assoc_dict = get_assoc_dict()
    categories = set()
    for match in re.finditer(r"\w+", f"{question} {content}"):
        word = match[0]
        if word in assoc_dict:
            categories |= assoc_dict[word]
    if not categories:
        categories.add("general")
    categories = " ".join(sorted(categories))

    db.execute(
        (
            "INSERT INTO questions (question, content, authorName, categories)"
            " VALUES (?, ?, ?, ?)"
        ),
        [question, content, author_name, categories],
    )
    db.commit()

    last_row_id = (
        db.execute("SELECT LAST_INSERT_ROWID()")
        .fetchone()["LAST_INSERT_ROWID()"]
    )

    for category in categories.split():
        role = category_to_role[category]
        for row in db.execute(
            "SELECT * FROM users WHERE role = ?",
            [role],
        ).fetchall():
            try:
                send_email(to=row["email"])
            except Exception as e:
                # Just in case the email doesn't exist (like during dev)
                print(repr(e))

    return {"id": last_row_id}, 200

@bp.route("/questions", methods=["GET", "POST"])
def questions_all():
    try:
        db = get_db()

        if request.method == "GET":
            rows = db.execute("SELECT * FROM questions").fetchall()

            response = jsonify([format_question(row) for row in rows])
            response.status_code = 200
            return response

        else:
            data = request.get_json(force=True)
            return _add_question(data)

    except Exception as e:
        return str(e), 400

@bp.route("/questions/<int:question_id>", methods=["GET"])
def questions_single(question_id):
    try:
        db = get_db()

        row = db.execute(
            "SELECT * FROM questions WHERE id = ?",
            [question_id],
        ).fetchone()

        if row is None:
            raise ValueError("question not found")

        return format_question(row), 200

    except Exception as e:
        return str(e), 400

@bp.route("/answer", methods=["POST"])
def answer():
    try:
        db = get_db()

        data = request.get_json(force=True)
        question_id = data["id"]
        content = data["content"]
        role = data["role"]
        author_name = data["authorName"]

        db.execute(
            (
                "INSERT INTO answers (questionId, content, role, authorName)"
                " VALUES (?, ?, ?, ?)"
            ),
            [question_id, content, role, author_name],
        )
        db.commit()

        last_row_id = (
            db.execute("SELECT LAST_INSERT_ROWID()")
            .fetchone()["LAST_INSERT_ROWID()"]
        )
        return {"id": last_row_id}, 200

    except Exception as e:
        return str(e), 400

@bp.route("/answers/<int:answer_id>", methods=["GET"])
def answer_single(answer_id):
    try:
        db = get_db()

        row = db.execute(
            "SELECT * FROM answer WHERE id = ?",
            [answer_id],
        ).fetchone()

        if row is None:
            raise ValueError("answer not found")

        return format_answer(row), 200

    except Exception as e:
        return str(e), 400
