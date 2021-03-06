from flask import Flask, current_app, logging
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from loadsongs import load_song_lists, raw_songdata
from flask_mail import Mail
from app.config import Config

songlist_pairs, lengthtype_pairs = load_song_lists()

difficulties = []
coop = ["2P", "3P", "4P", "5P"]
for i in range(1, 29):
    difficulties.append(str(i))
for i in coop:
    difficulties.append(i)
difficulties = list(zip(difficulties, difficulties))

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'success'

mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from app.users.routes import users
    from app.scores.routes import scores
    from app.main.routes import main
    from app.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(scores)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
