from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from auth import authorize_owner
from models.deck_card import DeckCard, DeckCardSchema
from models.deck import Deck
from init import db
import json


deck_cards_bp = Blueprint("deck_cards", __name__, url_prefix="/decks/<int:deck_id>/deck_cards")

# Get all deck cards for specified deck ID
@deck_cards_bp.route("/", methods=["GET"])
def all_deck_cards(deck_id):
    stmt = db.select(DeckCard).where(DeckCard.deck_id == deck_id)
    deck_cards = db.session.scalars(stmt).all()
    return DeckCardSchema(many=True).dump(deck_cards)

# Get one deck card for specified deck ID
@deck_cards_bp.route("/<int:id>", methods=["GET"])
def one_deck_card(deck_id, id):
    deck_card = db.session.query(DeckCard).filter_by(deck_id=deck_id, id=id).first_or_404()
    return DeckCardSchema().dump(deck_card)

# Create a new deck card for specified deck ID
@deck_cards_bp.route("/", methods=["POST"])
@jwt_required()
def create_deck_cards(deck_id):
    deck = db.get_or_404(Deck, deck_id)
    authorize_owner(deck)
    deck_card_list = request.json  # Expecting a list of {"card_id": int}
    created_deck_cards = []

    for deck_card_info in deck_card_list:
        deck_card = DeckCard(
            deck_id = deck_id,
            card_id = deck_card_info["card_id"]
        )
        db.session.add(deck_card)
        created_deck_cards.append(deck_card)

    db.session.commit()
    return DeckCardSchema(many=True).dump(created_deck_cards), 201

# Update an existing deck card
@deck_cards_bp.route("/<int:id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_deck_card(deck_id, id):
    deck_card = db.session.query(DeckCard).filter_by(deck_id=deck_id, id=id).first_or_404()
    authorize_owner(deck_card.deck)
    deck_card_info = DeckCardSchema(only=["card_id"], unknown="exclude").load(request.json)
    deck_card.card_id = deck_card_info["card_id"]
    db.session.commit()
    return DeckCardSchema().dump(deck_card)

# Delete an existing deck card
@deck_cards_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_deck_card(deck_id, id):
    deck_card = db.session.query(DeckCard).filter_by(deck_id=deck_id, id=id).first_or_404()
    authorize_owner(deck_card.deck)
    db.session.delete(deck_card)
    db.session.commit()
    return {}, 204