from os import environ
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt


app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = environ.get("JWT_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("DB_URI")

db = SQLAlchemy()
db.init_app(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)