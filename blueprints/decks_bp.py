from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from auth import authorize_owner
from models.deck import Deck, DeckSchema
from init import db

decks_bp = Blueprint("decks", __name__, url_prefix="/decks")

# Get all decks
@decks_bp.route("/", methods=["GET"])
def all_decks():
    stmt = db.select(Deck)
    decks = db.session.scalars(stmt).all()
    return DeckSchema(many=True).dump(decks)

# Get one deck
@decks_bp.route("/<int:id>", methods=["GET"])
def one_deck(id):
    deck = db.get_or_404(Deck, id)
    return DeckSchema().dump(deck)

# Create a new deck
@decks_bp.route("/", methods=["POST"])
@jwt_required()
def create_deck():
    deck_info = DeckSchema(only=["name", "decktypes", "description"], unknown="exclude").load(
        request.json
    )
    deck = Deck(
        name=deck_info["name"],
        decktypes=deck_info.get["decktypes", ""],
        description=deck_info.get("description", ""),
        user_id=get_jwt_identity()
    )
    db.session.add(deck)
    db.session.commit()
    return DeckSchema().dump(deck), 201

# Update an existing deck
@decks_bp.route("/<int:id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_deck(id):
    deck = db.get_or_404(Deck, id)
    authorize_owner(deck)
    deck_info = DeckSchema(only=["name", "decktypes", "description"], unknown="exclude").load(
        request.json
    )
    if "name" in deck_info:
        deck.name = deck_info["name"]
    if "deck_types" in deck_info:
        deck.deck_types = deck_info["deck_types"]
    if "description" in deck_info:
        deck.description = deck_info["description"]
    db.session.commit()
    return DeckSchema().dump(deck)

# Delete an existing deck
@decks_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_deck(id):
    deck = db.get_or_404(Deck, id)
    authorize_owner(deck)
    db.session.delete(deck)
    db.session.commit()
    return {}, 204