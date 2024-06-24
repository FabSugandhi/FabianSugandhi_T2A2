from flask import Blueprint
from models.card import Card
from models.deck_card import DeckCard
from models.deck import Deck
from models.set import Set
from models.user import User
from init import app, db, bcrypt
import json

db_commands = Blueprint("db", __name__)

@db_commands.cli.command("create")
def create_db():
    db.drop_all()
    db.create_all()
    print("Table created.")

@db_commands.cli.command("seed")
def seed_db():
    
    users = [
        User(
            email="admin@email.com",
            password=bcrypt.generate_password_hash("admin").decode("utf8"),
            first_name="admin",
            last_name="admin",
            is_admin=True
        ),
        User(
            email="user1",
            password=bcrypt.generate_password_hash("user1").decode("utf8"),
            first_name="user",
            last_name="1",
            is_admin=False
        ),
        User(
            email="user2",
            password=bcrypt.generate_password_hash("user2").decode("utf8"),
            first_name="user",
            last_name="2",
            is_admin=False
        )
    ]

    db.session.add_all(users)
    db.session.commit()
    
    sets = []

    with open("./seed_json/set.json", 'r') as file:
        data = json.load(file)
        for item in data:
            set = Set(
                name=item["name"],
                series=item["series"]
            )
            sets.append(set)

    db.session.add_all(sets)
    db.session.commit()

    cards = []

    with open("./seed_json/cards.json", 'r') as file:
        data = json.load(file)
        for item in data:
            
            
            
            card = Card(
                card_id=item["card_id"],
                name=item["name"],
                type=item["supertype"],
                set_id=item["set_id"]
            )

            "card_id": "swshp-SWSH001",
            "name": "Grookey",
            "supertype": "Pokemon",
            "set_id": "swshp"
            sets.append(set)