from main import ma
from models.UserCertification import UserCertification
from marshmallow.validate import Length
from datetime import datetime

class UserCertificationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserCertification
    
    username = ma.String(required=True, validate=Length(min=4))
    cert_name = ma.String(required=True)
    description = ma.String(required=True)
    issuer = ma.String(required=True)
    date_obtained = ma.String(required=True)
    last_updated = ma.String(required=True,nullable=False, default=datetime.utcnow)


UserCertificationSchema = UserCertificationSchema()
UserCertificationSchemas = UserCertificationSchema(many=True)