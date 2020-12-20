from main import ma
from models.UserWorkHistory import UserWorkHistory
from marshmallow.validate import Length

class UserWorkHistorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserWorkHistory

    username = ma.String(required=True, validate=Length(min=4))
    job_title = ma.String(required=True)
    company = ma.String(required=True)
    city = ma.String(required=True)
    country = ma.String(required=True)
    date_start = ma.String(required=True)
    date_end = ma.String(required=True)
    last_updated = ma.String(required=True)

user_work_history_schema = UserWorkHistorySchema()
user_work_history_schemas = UserWorkHistorySchema(many=True)