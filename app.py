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
    from models import Level
    if Level.query.count() == 0:
        from content.seed import seed
        from flask import current_app
        seed(current_app._get_current_object())


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
