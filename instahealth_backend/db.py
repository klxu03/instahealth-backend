import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    if 'db' not in g:
        db = sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        db.row_factory = sqlite3.Row
        g.db = db
    return g.db

def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    with current_app.open_resource("schema.sql") as file:
        db.executescript(file.read().decode("utf8"))

    from . import questions
    # Default questions for testing
    example_questions = [
        {
            "id": 1,
            "question": 'Mild occasional lightheadedness',
            "content": 'I have mild occasional lightheadedness',
            "authorName": 'one',
            "role": 'patient',
        },
        {
            "id": 2,
            "question": 'Severe weight loss',
            "content": 'I have severe weight loss',
            "authorName": 'two',
            "role": 'patient',
        },
        {
            "id": 3,
            "question": 'Mild ringing in the ears',
            "content": 'I have mild ringing in the ears',
            "authorName": 'three',
            "role": 'patient',
        },
        {
            "id": 4,
            "question": 'Critical shortness of breath',
            "content": 'I have critical shortness of breath',
            "authorName": 'four',
            "role": 'patient',
        },
    ]
    for question in example_questions:
        questions._add_question(question)

@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clears ALL pre-existing data and creates new tables"""
    init_db()
    click.echo("Initializaed the database.")

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
