from main import ma
from models.Message import Message
from schemas.UserSchema import user_schema
from marshmallow.validate import Length
from datetime import datetime

class MessageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Message
    
    sender = ma.Nested(user_schema)
    receiver = ma.Nested(user_schema)
    content = ma.String(required=True)
    read = ma.Boolean(default=False)
    liked = ma.Boolean(default=False)
    sent_time = ma.String(required=True,nullable=False, default=datetime.utcnow)


message_schema = MessageSchema()
message_schemas = MessageSchema(many=True)