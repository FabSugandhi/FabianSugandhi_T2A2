from . import db
from werkzeug.security import generate_password_hash, check_password_hash

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    card_number = db.Column(db.String(20), nullable=False)
    booster_set = db.Column(db.String(80), nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    collections = db.relationship('Collection', backref='user', lazy=True)
    decks = db.relationship('Deck', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Collection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    user = db.relationship('User', backref=db.backref('collections', lazy=True))
    card = db.relationship('Card', backref=db.backref('collections', lazy=True))

class Deck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(80), nullable=False)

    user = db.relationship('User', backref=db.backref('decks', lazy=True))
    deck_cards = db.relationship('DeckCard', backref='deck', lazy=True)

class DeckCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    deck_id = db.Column(db.Integer, db.ForeignKey('deck.id'), nullable=False)
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    deck = db.relationship('Deck', backref=db.backref('deck_cards', lazy=True))
    card = db.relationship('Card', backref=db.backref('deck_cards', lazy=True))
