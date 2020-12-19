from main import ma
from models.User import User
from marshmallow.validate import Length

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_only = ["password"]
    username = ma.String(required=True, validate=Length(min=4))
    first_name = ma.String(required=True)
    last_name = ma.String(required=True)
    created_at = ma.String(required=True)
    dob = ma.String(required=True)
    email = ma.String(required=True)
    mobile = ma.String()
    city = ma.String(required=True)
    country = ma.String(required=True)
    password = ma.String(required=True)


user_schema = UserSchema()
users_schema = UserSchema(many=True)