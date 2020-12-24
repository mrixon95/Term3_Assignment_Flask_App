from main import ma
from models.UserCertification import UserCertification
from schemas.UserSchema import user_schema
from marshmallow.validate import Length
from datetime import datetime

class UserCertificationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserCertification
    
    cert_name = ma.String(required=True)
    description = ma.String(required=True)
    issuer = ma.String(required=True)
    date_obtained = ma.String(required=True)
    last_updated = ma.String(required=True,nullable=False, default=datetime.utcnow)
    user = ma.Nested(user_schema)


user_certification_schema = UserCertificationSchema()
user_certification_schemas = UserCertificationSchema(many=True)