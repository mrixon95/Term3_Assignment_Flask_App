from main import ma
from models.Connection import Connection
from schemas.ConnectionSchema import ConnectionSchema
from marshmallow.validate import Length

class ConnectionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Connection

    user_id_1 = ma.String(required=True, validate=Length(min=1))
    user_id_2 = ma.String(required=True, validate=Length(min=1))
    last_updated = ma.String(required=True, validate=Length(min=4))
    status = ma.String(required=True)

connection_schema = ConnectionSchema()
connections_schema = ConnectionSchema(many=True)