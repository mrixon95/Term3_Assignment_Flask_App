from main import ma
from models.UserMeeting import UserMeeting
from schemas.UserSchema import user_schema
from marshmallow.validate import Length
from datetime import datetime

class UserMeetingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserMeeting
    
    time_start = ma.String(required=True)
    time_end = ma.String(required=True)
    location = ma.String(required=True)
    subject = ma.String(required=True)
    description = ma.String(required=True)
    last_updated = ma.String(required=True,nullable=False, default=datetime.utcnow)
    user = ma.Nested(user_schema)


user_meeting_schema = UserMeetingSchema()
user_meeting_schemas = UserMeetingSchema(many=True)