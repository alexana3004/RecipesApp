from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'user.login'


def create_app(config_obj=Config):
    app = Flask(__name__)
    app.config.from_object(config_obj)

    from .views.main.routes import main
    from .views.user.routes import user
    from .views.recipes.routes import recipes
    from.views.errors.handlers import errors
    app.register_blueprint(main)
    app.register_blueprint(user)
    app.register_blueprint(recipes)
    app.register_blueprint(errors)

    login_manager.init_app(app)
    db.init_app(app)

    from .models import User, Recipe, Favourites, Review
    with app.app_context():
        db.create_all()

    return app
