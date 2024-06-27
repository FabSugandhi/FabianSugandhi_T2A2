from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from auth import admin_only
from models.card import Card, CardSchema
from init import app, db, bcrypt
import json

cards_bp = Blueprint("cards", __name__, url_prefix="/cards")

# Get all cards
@cards_bp.route("/", methods=["GET"], endpoint="all_cards")
def all_cards():
    stmt = db.select(Card)
    cards = db.session.scalars(stmt).all()
    return CardSchema(many=True).dump(cards)

# Get one card
@cards_bp.route("/<int:id>", methods=["GET"], endpoint="one_card")
def one_card(id):
    card = db.get_or_404(Card, id)
    return CardSchema().dump(card)

# Create a new card
@cards_bp.route("/", methods=["POST"], endpoint="create_card")
@admin_only
def create_card():
    card_info = CardSchema(only=["card_id", "name", "type", "set_id"], unknown="exclude").load(
        request.json
    )
    card = Card(
        card_id=card_info["card_id"],
        name=card_info["name"],
        type=card_info["type"],
        set_id=card_info["set_id"]
    )
    db.session.add(card)
    db.session.commit()
    return CardSchema().dump(card), 201

# Update an existing card
@cards_bp.route("/<int:id>", methods=["PUT", "PATCH"], endpoint="update_card")
@admin_only
def update_card(id):
    card = db.get_or_404(Card, id)
    card_info = CardSchema(only=["card_id", "name", "type", "set_id"], unknown="exclude").load(
        request.json
    )
    # Update the attributes of the existing card object
    card.card_id = card_info["card_id"]
    card.name = card_info["name"]
    card.type = card_info["type"]
    card.set_id = card_info["set_id"]

    db.session.commit()
    return CardSchema().dump(card)

# Delete an existing card
@cards_bp.route("/<int:id>", methods=["DELETE"], endpoint="delete_card")
@admin_only
def delete_card(id):
    card = db.get_or_404(Card, id)
    db.session.delete(card)
    db.session.commit()
    return {}