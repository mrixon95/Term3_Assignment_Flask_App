from main import ma
from models.WorkHistory import WorkHistory
from schemas.UserSchema import user_schema
from marshmallow.validate import Length

class WorkHistorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = WorkHistory

    job_title = ma.String(required=True)
    company = ma.String(required=True)
    city = ma.String(required=True)
    country = ma.String(required=True)
    date_start = ma.String(required=True)
    date_end = ma.String(required=True)
    last_updated = ma.String(required=True)
    user = ma.Nested(user_schema)
    

work_history_schema = WorkHistorySchema()
work_history_schemas = WorkHistorySchema(many=True)