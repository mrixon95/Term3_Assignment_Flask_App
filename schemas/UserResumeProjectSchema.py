from main import ma
from models.UserResumeProject import UserResumeProject
from schemas.UserSchema import user_schema
from marshmallow.validate import Length

class UserResumeProjectSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserResumeProject

    resume_path = ma.String(required=True)
    github_account = ma.String(required=True)
    last_updated = ma.String(required=True)
    user = ma.Nested(user_schema)

user_resume_project_schema = UserResumeProjectSchema()
user_resume_project_schemas = UserResumeProjectSchema(many=True)