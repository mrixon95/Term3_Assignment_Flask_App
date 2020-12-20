from main import ma
from models.UserStudyHistory import UserStudyHistory
from marshmallow.validate import Length
from datetime import datetime

class UserStudyHistorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserStudyHistory
    
    username = ma.String(required=True, validate=Length(min=4))
    qualification_title = ma.String(required=True)
    institution = ma.String(required=True)
    city = ma.String(required=True)
    country = ma.String(required=True)
    date_start = ma.String(required=True)
    date_end = ma.String(required=True)
    last_updated = ma.String(required=True,nullable=False, default=datetime.utcnow)


user_study_history_schema = UserStudyHistorySchema()
user_study_history_schemas = UserStudyHistorySchema(many=True)