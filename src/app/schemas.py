from marshmallow import Schema, fields
from mashmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from .models import User, Card, Collection, Deck, DeckCard

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

class CardSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Card
        load_instance = True

class CollectionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Collection
        load_instance = True

class DeckSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Deck
        load_instance = True

class DeckCardSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = DeckCard
        load_instance = True
