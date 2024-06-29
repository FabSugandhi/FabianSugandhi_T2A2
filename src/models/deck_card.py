from init import db, ma
from marshmallow import fields

class DeckCard(db.Model):
    # define the table name for the db
    __tablename__= "deck_cards"
    # Set the primary key.
    id = db.Column(db.Integer,primary_key=True)

    # Foreign keys
    deck_id = db.Column(db.Integer, db.ForeignKey("decks.id", ondelete='CASCADE'), nullable=False)
    card_id = db.Column(db.Integer, db.ForeignKey("cards.id", ondelete='CASCADE'), nullable=False)

    # define the relationships
    deck = db.relationship(
        "Deck",
        back_populates="deck_cards",
    )
    card = db.relationship(
        "Card",
        back_populates="deck_cards",
    )

class DeckCardSchema(ma.Schema):
    deck_id = fields.Integer()
    card_id = fields.Integer()
    deck = fields.Nested("DeckSchema", only={"name"})
    card = fields.Nested("CardSchema", only={"name"})

    class Meta:
        ordered = True
        fields = ("id", "deck_id", "card_id", "deck", "card")