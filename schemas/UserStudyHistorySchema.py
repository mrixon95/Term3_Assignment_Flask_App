from main import ma
from models.UserStudyHistory import UserStudyHistory
from schemas.UserSchema import user_schema
from marshmallow.validate import Length
from datetime import datetime

class UserStudyHistorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserStudyHistory
    
    qualification_title = ma.String(required=True)
    institution = ma.String(required=True)
    city = ma.String(required=True)
    country = ma.String(required=True)
    date_start = ma.DateTime(required=True)
    date_end = ma.DateTime(required=True)
    last_updated = ma.DateTime(required=True)
    username = ma.Nested(user_schema)


user_study_history_schema = UserStudyHistorySchema()
user_study_history_schemas = UserStudyHistorySchema(many=True)