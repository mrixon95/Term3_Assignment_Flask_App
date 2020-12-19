from main import ma
from models.UserMeeting import UserStudyHistory
from marshmallow.validate import Length
from datetime import datetime

class UserMeetingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserStudyHistory
    
    username = ma.String(required=True, validate=Length(min=4))
    time_start = ma.String(required=True)
    time_end = ma.String(required=True)
    location = ma.String(required=True)
    subject = ma.String(required=True)
    description = ma.String(required=True)
    last_updated = ma.String(required=True,nullable=False, default=datetime.utcnow)


UserMeetingSchema = UserMeetingSchema()
UserMeetingSchemas = UserMeetingSchema(many=True)