from main import ma
from models.StudyHistory import StudyHistory
from schemas.UserSchema import user_schema
from marshmallow.validate import Length
from datetime import datetime

class StudyHistorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = StudyHistory
    
    qualification_title = ma.String(required=True)
    institution = ma.String(required=True)
    city = ma.String(required=True)
    country = ma.String(required=True)
    date_start = ma.DateTime(required=True)
    date_end = ma.DateTime(required=True)
    last_updated = ma.DateTime(required=True)
    user = ma.Nested(user_schema)


study_history_schema = StudyHistorySchema()
study_history_schemas = StudyHistorySchema(many=True)