from main import ma
from models.Certification import Certification
from schemas.UserSchema import user_schema
from marshmallow.validate import Length
from datetime import datetime

class CertificationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Certification
    
    cert_name = ma.String(required=True)
    description = ma.String(required=True)
    issuer = ma.String(required=True)
    date_obtained = ma.String(required=True)
    last_updated = ma.String(required=True,nullable=False, default=datetime.utcnow)
    user = ma.Nested(user_schema)


certification_schema = CertificationSchema()
certification_schemas = CertificationSchema(many=True)