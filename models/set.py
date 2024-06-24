from init import db, ma
from marshmallow import fields

class Set(db.Model):
    # define the table name for the db
    __tablename__= "sets"
    # Set the primary key.
    id = db.Column(db.Integer,primary_key=True)
    # Add the rest of the attributes. 
    name = db.Column(db.String(), nullable=False)
    series = db.Column(db.String(), nullable=False)

    # define the relationships
    cards = db.relationship(
        "Card",
        back_populates="set",
        cascade="all, delete"
    )

class SetSchema(ma.Schema):
    name = fields.String(required=True)
    series = fields.String(required=True)

    class Meta:
        ordered = True
        fields = ("id", "name", "series")