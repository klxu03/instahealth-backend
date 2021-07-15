from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db

bp = Blueprint("questions", __name__)

@bp.route("/questions", methods=["GET", "POST"])
def questions_all():
    try:
        db = get_db()

        if request.method == "GET":
            rows = db.execute("SELECT * FROM questions").fetchall()

            response = jsonify([
                {
                    key: row[key]
                    for key in [
                        "id",
                        "question",
                        "content",
                        "authorName",
                        "datePosted",
                    ]
                }
                for row in rows
            ])
            response.status_code = 200
            return response

        else:
            data = request.get_json(force=True)
            question = data["question"]
            content = data["content"]
            author_name = data["authorName"]

            db.execute(
                (
                    "INSERT INTO questions (question, content, authorName)"
                    " VALUES (?, ?, ?)"
                ),
                [question, content, author_name],
            )
            db.commit()

            return "", 200

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

        return {
            key: row[key]
            for key in [
                "id",
                "question",
                "content",
                "authorName",
                "datePosted",
            ]
        }, 200

    except Exception as e:
        return str(e), 400
