from . import db

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    card_number = db.Column(db.String(20), nullable=False)
    booster_set = db.Column(db.String(80), nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

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

class DeckCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    deck_id = db.Column(db.Integer, db.ForeignKey('deck.id'), nullable=False)
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    deck = db.relationship('Deck', backref=db.backref('deck_cards', lazy=True))
    card = db.relationship('Card', backref=db.backref('deck_cards', lazy=True))