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
    db.reflect()
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
            email="user1@email.com",
            password=bcrypt.generate_password_hash("user1").decode("utf8"),
            first_name="user",
            last_name="1",
            is_admin=False
        ),
        User(
            email="user2@email.com",
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

    set_mapping = {
        "swshp": 1,
        "swsh45": 2,
        "swsh5": 3,
        "swsh6": 4,
        "swsh7": 5,
        "cel25": 6,
        "swsh8": 7,
        "fut20": 8,
        "swsh9": 9,
        "swsh9tg": 10,
        "swsh10": 11,
        "swsh10tg": 12,
        "pgo": 13,
        "swsh11": 14,
        "swsh11tg": 15,
        "swsh12": 16,
        "swsh12tg": 17,
        "mcd22": 18,
        "swsh12pt5": 19,
        "swsh12pt5gg": 20,
        "sv1": 21,
        "svp": 22,
        "sv2": 23,
        "sve": 24,
        "sv3": 25,
        "sv3pt5": 26,
        "sv4": 27,
        "sv4pt5": 28,
        "sv5": 29,
        "sv6": 30
    }

    cards = []

    with open("./seed_json/cards.json", 'r') as file:
        data = json.load(file)
        for item in data:
            set_id = set_mapping.get(item["set_id"])

            if set_id is None:
                raise ValueError(f"Unknown set id: {item['set_id']}")

            card = Card(
                card_id=item["card_id"],
                name=item["name"],
                type=item["supertype"],
                set_id=set_id
            )
            cards.append(card)
            
    db.session.add_all(cards)
    db.session.commit()

    print("Table seeded")