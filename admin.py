from datetime import datetime, timedelta

from flask import Blueprint, abort, render_template
from flask_login import current_user, login_required
from sqlalchemy import func

from extensions import db
from models import Level, User, UserProgress

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def _require_admin():
    from flask import current_app
    if not current_user.is_authenticated:
        abort(401)
    if current_user.email not in current_app.config["ADMIN_EMAILS"]:
        abort(403)


@admin_bp.route("/")
@login_required
def dashboard():
    _require_admin()
    now = datetime.utcnow()

    total_users = User.query.count()
    users_today = User.query.filter(
        func.date(User.created_at) == now.date()
    ).count()
    users_this_week = User.query.filter(
        User.created_at >= now - timedelta(days=7)
    ).count()
    users_this_month = User.query.filter(
        User.created_at >= now - timedelta(days=30)
    ).count()
    active_users = User.query.filter(
        User.last_active >= now - timedelta(days=7)
    ).count()

    # Daily signups — last 14 days
    signup_data = []
    for i in range(13, -1, -1):
        day = (now - timedelta(days=i)).date()
        count = User.query.filter(func.date(User.created_at) == day).count()
        signup_data.append({"date": day.strftime("%b %d"), "count": count})

    # Per-level stats
    levels = Level.query.order_by(Level.id).all()
    level_stats = []
    for lev in levels:
        completions = UserProgress.query.filter_by(level_id=lev.id, passed=True).count()
        attempts = UserProgress.query.filter_by(level_id=lev.id).count()
        level_stats.append(
            {
                "level": lev,
                "completions": completions,
                "attempts": attempts,
                "rate": round(completions / attempts * 100) if attempts else 0,
            }
        )

    recent_users = User.query.order_by(User.created_at.desc()).limit(15).all()

    return render_template(
        "admin/dashboard.html",
        total_users=total_users,
        users_today=users_today,
        users_this_week=users_this_week,
        users_this_month=users_this_month,
        active_users=active_users,
        signup_data=signup_data,
        level_stats=level_stats,
        recent_users=recent_users,
    )
