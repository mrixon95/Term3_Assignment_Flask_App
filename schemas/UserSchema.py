from main import ma
from models.User import User
from marshmallow.validate import Length, Email

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_only = ["password"]
    username = ma.String(required=True, validate=Length(min=4))
    first_name = ma.String(required=True, validate=Length(min=2))
    last_name = ma.String(required=True, validate=Length(min=2))
    created_at = ma.String(required=True)
    dob = ma.String(required=True)
    email = ma.String(required=True, validate=Email())
    mobile = ma.String()
    city = ma.String(required=True)
    country = ma.String(required=True)
    password = ma.String(required=True)


user_schema = UserSchema()
user_schemas = UserSchema(many=True)