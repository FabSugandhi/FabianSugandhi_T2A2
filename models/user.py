from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length

class User(db.Model):
    # define the table name for the db
    __tablename__= "users"
    # Set the primary key.
    id = db.Column(db.Integer,primary_key=True)
    # Add the rest of the attributes. 
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    is_admin = db.Column(db.Boolean(), default=False)

    # define the relationships
    decks = db.relationship(
        "Deck",
        back_populates="user",
        cascade="all, delete"
    ) 

class UserSchema(ma.Schema):
    email = fields.Email(required=True)
    password = fields.String(validate=Length(min=4, error="Password must be at least 4 characters"), required=True)
    first_name = fields.String(required=True)

    decks = fields.Nested("DeckSchema", many=True)

    class Meta:
        ordered = True
        fields = ("id", "email", "password", "first_name", "last_name", "is_admin", "decks")