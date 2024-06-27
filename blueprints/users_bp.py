from datetime import timedelta
from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from auth import admin_only
from models.user import User, UserSchema
from init import app, db, bcrypt
import json

users_bp = Blueprint("users", __name__, url_prefix="/users")

# User login
@users_bp.route("/login", methods=["POST"])
def login():
    # Get the email and password from the request
    params = UserSchema(only=["email", "password"]).load(
        request.json, unknown="exclude"
    )
    # Compare email and password against db
    stmt = db.select(User).where(User.email == params["email"])
    user = db.session.scalar(stmt)
    if user and bcrypt.check_password_hash(user.password, params["password"]):
        # Generate the JWT
        token = create_access_token(identity=user.id, expires_delta=timedelta(hours=2))
        # Return the JWT
        return {"token": token}
    else:
        # Error handling (user not found, wrong username or wrong password)
        return {"error": "Invalid email or password"}, 401

# Create a new user, only admin for testing purposes
@users_bp.route('/', methods=['POST'])
@admin_only
def create_user():
    user_info = UserSchema(only=["email", "password", "first_name", "last_name", "is_admin"]).load(request.json)

    user = User(
        email=user_info["email"],
        password=bcrypt.generate_password_hash(user_info["password"]).decode("utf8"),
        first_name=user_info["first_name"],
        last_name=user_info["last_name"],
        is_admin=user_info["is_admin"]
    )
    
    db.session.add(user)
    db.session.commit()
    return UserSchema().dump(user), 201