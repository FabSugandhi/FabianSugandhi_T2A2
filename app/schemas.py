from marshmallow import Schema, fields, post_load
from .models import User, Card, Collection, Deck, DeckCard

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(load_only=True, required=True)

    @post_load
    def make_user(self, data, **kwargs):
        user = User(**data)
        user.set_password(data['password'])
        return user

class CardSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    card_number = fields.Str(required=True)
    booster_set = fields.Str(required=True)

class CollectionSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    card_id = fields.Int(required=True)
    quantity = fields.Int(required=True)

class DeckSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    name = fields.Str(required=True)

class DeckCardSchema(Schema):
    id = fields.Int(dump_only=True)
    deck_id = fields.Int(required=True)
    card_id = fields.Int(required=True)
    quantity = fields.Int(required=True)
