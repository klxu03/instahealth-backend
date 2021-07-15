from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db
from .assoc import get_assoc_dict

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
            "tags",
            "datePosted",
        ]
    }

    question_id = data["id"]
    rows = db.execute(
        "SELECT * FROM answers WHERE questionId = ?",
        [question_id],
    ).fetchall()
    answers = data["answers"] = []
    for row in rows:
        answers.append({
            key: row[key]
            for key in [
                "id",
                "content",
                "authorName",
                "role",
                "datePosted",
            ]
        })

    return data

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
            question = data["question"]
            content = data["content"]
            author_name = data["authorName"]

            assoc_dict = get_assoc_dict()
            tags = set()
            for match in re.finditer(r"\w+", f"{question} {content}"):
                word = match[0]
                if word in assoc_dict:
                    tags |= assoc_dict[word]
            tags = " ".join(sorted(tags))

            db.execute(
                (
                    "INSERT INTO questions (question, content, authorName, tags)"
                    " VALUES (?, ?, ?, ?)"
                ),
                [question, content, author_name, tags],
            )
            db.commit()

            last_row_id = (
                db.execute("SELECT LAST_INSERT_ROWID()")
                .fetchone()["LAST_INSERT_ROWID()"]
            )
            return {"id": last_row_id}, 200

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
