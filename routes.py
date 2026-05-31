from datetime import datetime

from flask import Blueprint, abort, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from extensions import db
from models import Flashcard, Level, Question, UserProgress

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def landing():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    return render_template("landing.html")


@main_bp.route("/home")
@login_required
def home():
    levels = Level.query.order_by(Level.id).all()
    progress_map = {
        p.level_id: p
        for p in UserProgress.query.filter_by(user_id=current_user.id).all()
    }

    level_data = []
    for level in levels:
        p = progress_map.get(level.id)
        if p and p.passed:
            status = "completed"
        elif level.id == 1 or (progress_map.get(level.id - 1) and progress_map[level.id - 1].passed):
            status = "available"
        else:
            status = "locked"
        level_data.append({"level": level, "status": status, "progress": p})

    completed_count = sum(1 for l in level_data if l["status"] == "completed")
    total_xp = sum(l["level"].xp_reward for l in level_data if l["status"] == "completed")

    return render_template(
        "home.html",
        level_data=level_data,
        completed_count=completed_count,
        total_xp=total_xp,
    )


@main_bp.route("/level/<int:level_id>")
@login_required
def level(level_id):
    lev = Level.query.get_or_404(level_id)

    if level_id > 1:
        prev = UserProgress.query.filter_by(
            user_id=current_user.id, level_id=level_id - 1
        ).first()
        if not prev or not prev.passed:
            abort(403)

    flashcards = (
        Flashcard.query.filter_by(level_id=level_id).order_by(Flashcard.order).all()
    )
    progress = UserProgress.query.filter_by(
        user_id=current_user.id, level_id=level_id
    ).first()

    return render_template("level.html", level=lev, flashcards=flashcards, progress=progress)


@main_bp.route("/level/<int:level_id>/complete", methods=["POST"])
@login_required
def complete_flashcards(level_id):
    Level.query.get_or_404(level_id)

    progress = UserProgress.query.filter_by(
        user_id=current_user.id, level_id=level_id
    ).first()
    if not progress:
        progress = UserProgress(user_id=current_user.id, level_id=level_id)
        db.session.add(progress)

    progress.flashcards_seen = True
    db.session.commit()
    return redirect(url_for("main.quiz", level_id=level_id))


@main_bp.route("/level/<int:level_id>/quiz")
@login_required
def quiz(level_id):
    lev = Level.query.get_or_404(level_id)

    progress = UserProgress.query.filter_by(
        user_id=current_user.id, level_id=level_id
    ).first()
    if not progress or not progress.flashcards_seen:
        return redirect(url_for("main.level", level_id=level_id))

    questions = (
        Question.query.filter_by(level_id=level_id).order_by(Question.order).all()
    )
    questions_data = [
        {
            "id": q.id,
            "type": q.type,
            "stem": q.stem,
            "options": q.options,
            "answer": q.answer,
            "explanation": q.explanation or "",
        }
        for q in questions
    ]

    return render_template("quiz.html", level=lev, questions_data=questions_data, progress=progress)


@main_bp.route("/level/<int:level_id>/quiz", methods=["POST"])
@login_required
def submit_quiz(level_id):
    questions = Question.query.filter_by(level_id=level_id).all()
    answers = request.get_json() or {}

    correct = 0
    results = []
    for q in questions:
        user_ans = answers.get(str(q.id), "").strip().lower()
        correct_ans = q.answer.strip().lower()
        is_correct = user_ans == correct_ans
        if is_correct:
            correct += 1
        results.append(
            {
                "question_id": q.id,
                "correct": is_correct,
                "user_answer": answers.get(str(q.id), ""),
                "correct_answer": q.answer,
                "explanation": q.explanation or "",
            }
        )

    total = len(questions)
    score = correct / total if total else 0
    passed = score >= 0.7

    progress = UserProgress.query.filter_by(
        user_id=current_user.id, level_id=level_id
    ).first()
    if not progress:
        progress = UserProgress(user_id=current_user.id, level_id=level_id)
        db.session.add(progress)

    progress.attempts += 1
    if progress.quiz_score is None or score > progress.quiz_score:
        progress.quiz_score = score
    if passed and not progress.passed:
        progress.passed = True
        progress.completed_at = datetime.utcnow()

    db.session.commit()

    lev = Level.query.get(level_id)
    return jsonify(
        {
            "score": score,
            "correct": correct,
            "total": total,
            "passed": passed,
            "xp": lev.xp_reward if passed else 0,
            "results": results,
        }
    )
