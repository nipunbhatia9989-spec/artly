from datetime import datetime
from flask_login import UserMixin
from extensions import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    picture = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_active = db.Column(db.DateTime, default=datetime.utcnow)

    progress = db.relationship("UserProgress", backref="user", lazy=True)


class Level(db.Model):
    __tablename__ = "levels"

    id = db.Column(db.Integer, primary_key=True)  # 1–50
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    difficulty = db.Column(db.Integer, default=1)  # 1–5
    topic = db.Column(db.String(200))
    wikipedia_article = db.Column(db.String(200))
    xp_reward = db.Column(db.Integer, default=10)

    flashcards = db.relationship(
        "Flashcard", backref="level", lazy=True, order_by="Flashcard.order"
    )
    questions = db.relationship(
        "Question", backref="level", lazy=True, order_by="Question.order"
    )


class Flashcard(db.Model):
    __tablename__ = "flashcards"

    id = db.Column(db.Integer, primary_key=True)
    level_id = db.Column(db.Integer, db.ForeignKey("levels.id"), nullable=False)
    front = db.Column(db.Text, nullable=False)
    back = db.Column(db.Text, nullable=False)
    order = db.Column(db.Integer, default=0)


class Question(db.Model):
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    level_id = db.Column(db.Integer, db.ForeignKey("levels.id"), nullable=False)
    # type: mcq (4 options) | single (2 options) | yesno | fill (free text)
    type = db.Column(db.String(20), nullable=False)
    stem = db.Column(db.Text, nullable=False)
    options = db.Column(db.JSON)  # list of strings; null for fill
    answer = db.Column(db.String(500), nullable=False)
    explanation = db.Column(db.Text)
    order = db.Column(db.Integer, default=0)


class UserProgress(db.Model):
    __tablename__ = "user_progress"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    level_id = db.Column(db.Integer, db.ForeignKey("levels.id"), nullable=False)
    flashcards_seen = db.Column(db.Boolean, default=False)
    quiz_score = db.Column(db.Float)  # best score, 0.0–1.0
    passed = db.Column(db.Boolean, default=False)
    attempts = db.Column(db.Integer, default=0)
    completed_at = db.Column(db.DateTime)

    __table_args__ = (db.UniqueConstraint("user_id", "level_id"),)


class Feedback(db.Model):
    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    level_id = db.Column(db.Integer, db.ForeignKey("levels.id"), nullable=False)
    target_type = db.Column(db.String(10), nullable=False)  # "card" or "level"
    target_id = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.String(4))  # "up" or "down" or None
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
