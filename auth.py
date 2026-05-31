from datetime import datetime

from flask import Blueprint, redirect, url_for
from flask_login import login_user, logout_user

from extensions import db, oauth
from models import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login")
def login():
    redirect_uri = url_for("auth.callback", _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@auth_bp.route("/callback")
def callback():
    token = oauth.google.authorize_access_token()
    info = token["userinfo"]

    user = User.query.filter_by(google_id=info["sub"]).first()
    if user:
        user.last_active = datetime.utcnow()
    else:
        user = User(
            google_id=info["sub"],
            email=info["email"],
            name=info["name"],
            picture=info.get("picture"),
        )
        db.session.add(user)

    db.session.commit()
    login_user(user, remember=True)
    return redirect(url_for("main.home"))


@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.landing"))
