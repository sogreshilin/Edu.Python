from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from config import Config

db = SQLAlchemy()
login = LoginManager()
login.login_view = 'auth.login'
bootstrap = Bootstrap()
app = Flask(__name__)


def create_app(config_class=Config):
    app.config.from_object(Config)

    db.init_app(app)
    login.init_app(app)
    bootstrap.init_app(app)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app