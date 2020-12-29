from main import ma
from models.Meeting import Meeting
from schemas.UserSchema import user_schema
from marshmallow.validate import Length
from datetime import datetime

class MeetingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Meeting
    
    time_start = ma.String(required=True)
    time_end = ma.String(required=True)
    location = ma.String(required=True)
    subject = ma.String(required=True)
    description = ma.String(required=True)
    last_updated = ma.String(required=True,nullable=False, default=datetime.utcnow)
    user = ma.Nested(user_schema)


meeting_schema = MeetingSchema()
meeting_schemas = MeetingSchema(many=True)