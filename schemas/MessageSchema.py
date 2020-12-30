from main import ma
from models.Message import Message
from schemas.UserSchema import user_schema
from marshmallow import validate
from datetime import datetime

class MessageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Message
    
    sender = ma.Nested(user_schema)
    receiver = ma.Nested(user_schema)
    content = ma.String(required=True, validate=validate.Length(min=10))
    read = ma.Boolean(default=False)
    liked = ma.Boolean(default=False)
    sent_time = ma.DateTime(required=True,nullable=False, default=datetime.utcnow)


message_schema = MessageSchema()
message_schemas = MessageSchema(many=True)