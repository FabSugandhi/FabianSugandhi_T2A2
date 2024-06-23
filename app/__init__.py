from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    with app.app_context():
        from .views import auth_bp, card_bp, collection_bp, deck_bp
        app.register_blueprint(auth_bp, url_prefix='/auth')
        app.register_blueprint(card_bp, url_prefix='/card')
        app.register_blueprint(collection_bp, url_prefix='/collection')
        app.register_blueprint(deck_bp, url_prefix='/deck')

    return app
