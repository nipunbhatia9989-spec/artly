from flask import Flask

from config import Config
from extensions import db, login_manager, oauth


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = ""

    oauth.init_app(app)
    oauth.register(
        name="google",
        client_id=app.config["GOOGLE_CLIENT_ID"],
        client_secret=app.config["GOOGLE_CLIENT_SECRET"],
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile"},
    )

    from auth import auth_bp
    from routes import main_bp
    from admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)

    @login_manager.user_loader
    def load_user(user_id):
        from models import User
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()
        _auto_seed()

    return app


def _auto_seed():
    _migrate()
    from models import Level
    if Level.query.count() == 0:
        from content.seed import seed
        from flask import current_app
        seed(current_app._get_current_object())
    else:
        _patch_images()


def _migrate():
    from sqlalchemy import text
    for stmt in [
        "ALTER TABLE flashcards ADD COLUMN image_url VARCHAR(500)",
        "ALTER TABLE feedback ADD COLUMN image_url VARCHAR(500)",  # no-op guard
    ]:
        try:
            db.session.execute(text(stmt))
            db.session.commit()
        except Exception:
            db.session.rollback()


def _patch_images():
    from models import Flashcard
    from content.seed_data import SEED
    if Flashcard.query.filter(Flashcard.image_url.isnot(None)).count() > 0:
        return
    for level_id, content in SEED.items():
        for i, card_data in enumerate(content["flashcards"]):
            if len(card_data) < 3 or not card_data[2]:
                continue
            fc = Flashcard.query.filter_by(level_id=level_id, order=i).first()
            if fc:
                fc.image_url = card_data[2]
    db.session.commit()


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
