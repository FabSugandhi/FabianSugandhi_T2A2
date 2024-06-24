from init import db, ma
from marshmallow import fields

class Deck(db.Model):
    # define the table name for the db
    __tablename__= "decks"
    # Set the primary key.
    id = db.Column(db.Integer,primary_key=True)
    # Add the rest of the attributes. 
    name = db.Column(db.String(), nullable=False)
    deck_types = db.Column(db.String())
    description = db.Column(db.String())
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # define the relationships
    user = db.relationship(
        "User",
        back_populates="decks",
        cascade="all, delete"
    )
    deck_cards = db.relationship(
        "DeckCard",
        back_populates="deck",
        cascade="all, delete"
    )

class DeckSchema(ma.Schema):
    name = fields.String(required=True)

    user = fields.Nested("UserSchema", only={"id", "first_name", "last_name"})
    deck_card = fields.Nested("DeckCardSchema", many=True)

    class Meta:
        ordered = True
        fields = ("id", "name", "deck_types", "description", "user")