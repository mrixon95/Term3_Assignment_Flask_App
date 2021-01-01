from main import ma
from models.Connection import Connection
from schemas.UserSchema import user_schema
from marshmallow.validate import Length, OneOf
from datetime import datetime

class ConnectionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Connection

    requester = ma.Nested(user_schema)
    confirmer = ma.Nested(user_schema)
    last_updated = ma.DateTime(default=datetime.utcnow)
    user_1_approved = ma.Boolean(default=True)
    user_2_approved = ma.Boolean(default=False)
    status = ma.String(default='pending', validate=[OneOf(["pending", "confirmed"])])

connection_schema = ConnectionSchema()
connection_schemas = ConnectionSchema(many=True)