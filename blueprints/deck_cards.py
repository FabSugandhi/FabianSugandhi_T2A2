from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from auth import admin_only, authorize_owner
from models.deck_card import DeckCard, DeckCardSchema
from init import app, db, bcrypt
import json


deck_cards_bp = Blueprint("deck_cards", __name__, url_prefix="/deck_cards")

# Get all deck cards
@deck_cards_bp.route("/", methods=["GET"])
def all_deck_cards():
    stmt = db.select(DeckCard)
    deck_cards = db.session.scalars(stmt).all()
    return DeckCardSchema(many=True).dump(deck_cards)

# Get one deck cards
@deck_cards_bp.route("/<int:id>", methods=["GET"])
def one_deck_card(id):
    deck_card = db.get_or_404(DeckCard, id)
    return DeckCardSchema().dump(deck_card)

# Create a new deck card
@deck_cards_bp.route("/", methods=["POST"])
@jwt_required()
def create_deck_card():
    deck_card_info = DeckCardSchema(only=["deck", "card"], unknown="exclude").load(
        request.json
    )
    deck_card = DeckCard(
        deck=deck_card_info["deck"],
        card=deck_card_info["card"],
    )
    db.session.add(deck_card)
    db.session.commit()
    return DeckCardSchema().dump(deck_card), 201

# Update an existing deck card
@deck_cards_bp.route("/<int:id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_deck_card(id):
    deck_card = db.get_or_404(DeckCard, id)
    authorize_owner(deck_card)
    deck_card_info = DeckCardSchema(only=["deck", "card"], unknown="exclude").load(
        request.json
    )
    deck_card = DeckCard(
        deck=deck_card_info["deck"],
        card=deck_card_info["card"],
    )
    db.session.commit()
    return DeckCardSchema().dump(deck_card)

# Delete an existing deck card
@deck_cards_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_deck_card(id):
    deck_card = db.get_or_404(DeckCard, id)
    authorize_owner(deck_card)
    db.session.delete(deck_card)
    db.session.commit()
    return {}