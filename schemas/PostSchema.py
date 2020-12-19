from main import ma
from models.Post import Post
from marshmallow.validate import Length
from datetime import datetime

class PostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Post
    
    username = ma.String(required=True, validate=Length(min=4))
    cert_name = ma.String(required=True)
    description = ma.String(required=True)
    issuer = ma.String(required=True)
    date_obtained = ma.String(required=True)
    last_updated = ma.String(required=True,nullable=False, default=datetime.utcnow)


PostSchema = PostSchema()
PostSchemas = PostSchema(many=True)