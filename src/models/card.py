from init import db, ma
from marshmallow import fields
from marshmallow.validate import OneOf

VALID_TYPES = ('Pokemon', 'Trainer', 'Energy')

class Card(db.Model):
    # define the table name for the db
    __tablename__= "cards"
    # Set the primary key.
    id = db.Column(db.Integer,primary_key=True)
    # Add the rest of the attributes. 
    card_id = db.Column(db.String(), unique=True, nullable=False)
    name = db.Column(db.String(), nullable=False)
    type = db.Column(db.String(), nullable=False)
    # Foreign keys
    set_id = db.Column(db.Integer, db.ForeignKey("sets.id"), nullable=False)

    # define the relationships
    set = db.relationship(
        "Set",
        back_populates="cards",
    )
    deck_cards = db.relationship(
        "DeckCard",
        back_populates="card",
        cascade="all, delete"
    )

class CardSchema(ma.Schema):
    card_id = fields.String(required=True)
    name = fields.String(required=True)
    type = fields.String(required=True, validate=OneOf(VALID_TYPES))

    set = fields.Nested("SetSchema", only={"name"})

    class Meta:
        ordered = True
        fields = ("id", "card_id", "name", "type", "set_id", "set")