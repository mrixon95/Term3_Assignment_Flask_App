from main import ma
from models.UserResumeProject import UserResumeProject
from marshmallow.validate import Length

class UserResumeProjectSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserResumeProject

    username = ma.String(required=True, validate=Length(min=4))
    resume_path = ma.String(required=True)
    github_account = ma.String(required=True)
    last_updated = ma.String(required=True)

UserResumeProjectSchema = UserResumeProjectSchema()
UserResumeProjectSchemas = UserResumeProjectSchema(many=True)