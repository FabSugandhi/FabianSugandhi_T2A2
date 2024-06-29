from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)
from init import db
from models.user import User
from flask import abort, jsonify, make_response
from functools import wraps

# Route decorator - ensure JWT user is an admin
def admin_only(fn):
    @wraps(fn)
    @jwt_required()
    def inner(*args, **kwargs):
        user_id = get_jwt_identity()
        stmt = db.select(User).where(User.id == user_id, User.is_admin)
        user = db.session.scalar(stmt)
        if user:
            return fn(*args, **kwargs)
        else:
            return {"error": "You must be an admin to access this resource"}, 403

    return inner

# Ensure that the JWT user is the owner of the given Deck
def authorize_owner(deck):
    user_id = get_jwt_identity()
    if user_id != deck.user_id:
        abort(make_response(jsonify(error="You must be the deck owner to access this resource"), 403))