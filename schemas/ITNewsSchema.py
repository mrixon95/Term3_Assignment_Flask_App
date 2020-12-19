from main import ma
from models.UserCertification import UserCertification
from marshmallow.validate import Length
from datetime import datetime

class ITNewsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserCertification
    
    article_link = ma.String(required=True)
    photo_link = ma.String(required=True)
    published_time = ma.String(required=True,nullable=False, default=datetime.utcnow)


ITNewsSchema = ITNewsSchema()
ITNewsSchemas = ITNewsSchema(many=True)