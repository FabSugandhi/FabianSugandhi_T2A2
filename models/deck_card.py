from init import db, ma
from marshmallow import fields

class DeckCard(db.Model):
    # define the table name for the db
    __tablename__= "deckcards"
    # Set the primary key.
    id = db.Column(db.Integer,primary_key=True)

    # Foreign keys
    deck_id = db.Column(db.Integer, db.ForeignKey("decks.id"), nullable=False)
    card_id = db.Column(db.Integer, db.ForeignKey("cards.id"), nullable=False)

    # define the relationships
    deck = db.relationship(
        "Deck",
        back_populates="deck_cards",
        cascade="all, delete"
    )
    card = db.relationship(
        "Card",
        back_populates="deck_cards",
        cascade="all, delete"
    )

class DeckCardSchema(ma.Schema):

    deck = fields.Nested("DeckSchema", only={"id", "name"})
    card = fields.Nested("CardSchema")

    class Meta:
        ordered = True
        fields = ("id", "deck", "card")