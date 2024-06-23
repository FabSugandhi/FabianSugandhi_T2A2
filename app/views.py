from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from .models import db, User, Card, Collection, Deck, DeckCard
from .schemas import UserSchema, CardSchema, CollectionSchema, DeckSchema, DeckCardSchema

user_schema = UserSchema()
card_schema = CardSchema()
collection_schema = CollectionSchema()
deck_schema = DeckSchema()
deck_card_schema = DeckCardSchema()

auth_bp = Blueprint('auth', __name__)
collection_bp = Blueprint('collection', __name__)
deck_bp = Blueprint('deck', __name__)
card_bp = Blueprint('card', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user, errors = user_schema.load(data)
    if errors:
        return jsonify(errors), 400
    db.session.add(user)
    db.session.commit()
    return user_schema.jsonify(user), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"msg": "Invalid username or password"}), 401
    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token), 200

@card_bp.route('/cards', methods=['POST'])
@jwt_required()
def create_card():
    data = request.get_json()
    card, errors = card_schema.load(data)
    if errors:
        return jsonify(errors), 400
    db.session.add(card)
    db.session.commit()
    return card_schema.jsonify(card), 201

@collection_bp.route('/collections', methods=['POST'])
@jwt_required()
def create_collection():
    data = request.get_json()
    data['user_id'] = get_jwt_identity()
    collection, errors = collection_schema.load(data)
    if errors:
        return jsonify(errors), 400
    db.session.add(collection)
    db.session.commit()
    return collection_schema.jsonify(collection), 201

@collection_bp.route('/collections', methods=['GET'])
@jwt_required()
def get_collection():
    user_id = get_jwt_identity()
    collection = Collection.query.filter_by(user_id=user_id).all()
    result = collection_schema.dump(collection, many=True)
    return jsonify(result), 200

@deck_bp.route('/decks', methods=['POST'])
@jwt_required()
def create_deck():
    data = request.get_json()
    data['user_id'] = get_jwt_identity()
    deck, errors = deck_schema.load(data)
    if errors:
        return jsonify(errors), 400
    db.session.add(deck)
    db.session.commit()
    return deck_schema.jsonify(deck), 201

@deck_bp.route('/decks/<int:deck_id>/cards', methods=['POST'])
@jwt_required()
def add_card_to_deck(deck_id):
    data = request.get_json()
    data['deck_id'] = deck_id
    deck_card, errors = deck_card_schema.load(data)
    if errors:
        return jsonify(errors), 400
    db.session.add(deck_card)
    db.session.commit()
    return deck_card_schema.jsonify(deck_card), 201
