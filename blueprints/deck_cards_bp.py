from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from auth import authorize_owner
from models.deck_card import DeckCard, DeckCardSchema
from models.deck import Deck
from init import db
import json


deck_cards_bp = Blueprint("deck_cards", __name__, url_prefix="/decks/<int:deck_id>/deck_cards")

# Get all deck cards for specified deck ID
@deck_cards_bp.route("/", methods=["GET"], endpoint="all_deck_cards")
def all_deck_cards(deck_id):
    stmt = db.select(DeckCard).where(DeckCard.deck_id == deck_id)
    deck_cards = db.session.scalars(stmt).all()
    return DeckCardSchema(many=True).dump(deck_cards)

# Get one deck card for specified deck ID
@deck_cards_bp.route("/<int:id>", methods=["GET"], endpoint="one_deck_card")
def one_deck_card(deck_id, id):
    deck_card = db.session.query(DeckCard).filter_by(deck_id=deck_id, id=id).first_or_404()
    return DeckCardSchema().dump(deck_card)

# Create a new deck card for specified deck ID
@deck_cards_bp.route("/", methods=["POST"], endpoint="create_deck_cards")
@jwt_required()
def create_deck_cards(deck_id):
    deck = db.get_or_404(Deck, deck_id)
    authorize_owner(deck)

    # Ensure request.json is properly formatted
    if not isinstance(request.json, list):
        return {"message": "Invalid JSON format. Expected a list of {'card_id': int} objects."}, 400
    
    created_deck_cards = []

    for deck_card_info in request.json:
        if not isinstance(deck_card_info, dict) or "card_id" not in deck_card_info:
            return {"message": "Invalid deck card format. Each object should contain a 'card_id' key."}, 400
        
        card_id = deck_card_info["card_id"]  # Ensure 'card_id' is accessed correctly
        deck_card = DeckCard(
            deck_id=deck_id,
            card_id=card_id
        )
        db.session.add(deck_card)
        created_deck_cards.append(deck_card)
    db.session.commit()

    # Return a response indicating successful creation
    return {"message": "Deck cards created successfully", "created_count": len(created_deck_cards)}, 201

# Update an existing deck card
@deck_cards_bp.route("/<int:id>", methods=["PUT", "PATCH"], endpoint="update_deck_cards")
@jwt_required()
def update_deck_card(deck_id, id):
    deck_card = db.session.query(DeckCard).filter_by(deck_id=deck_id, id=id).first_or_404()
    authorize_owner(deck_card.deck)
    deck_card_info = DeckCardSchema(only=["card_id"], unknown="exclude").load(request.json)
    deck_card.card_id = deck_card_info["card_id"]
    db.session.commit()
    return DeckCardSchema().dump(deck_card)

# Delete an existing deck card
@deck_cards_bp.route("/<int:id>", methods=["DELETE"], endpoint="delete_deck_cards")
@jwt_required()
def delete_deck_card(deck_id, id):
    deck_card = db.session.query(DeckCard).filter_by(deck_id=deck_id, id=id).first_or_404()
    authorize_owner(deck_card.deck)
    db.session.delete(deck_card)
    db.session.commit()
    return {}, 204