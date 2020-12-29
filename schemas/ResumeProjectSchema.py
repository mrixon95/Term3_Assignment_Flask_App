from main import ma
from models.ResumeProject import ResumeProject
from schemas.UserSchema import user_schema
from marshmallow.validate import Length

class ResumeProjectSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ResumeProject

    resume_path = ma.String(required=True)
    github_account = ma.String(required=True)
    last_updated = ma.String(required=True)
    user = ma.Nested(user_schema)

resume_project_schema = ResumeProjectSchema()
resume_project_schemas = ResumeProjectSchema(many=True)