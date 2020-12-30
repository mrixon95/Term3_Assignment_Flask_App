from main import ma
from models.Post import Post
from marshmallow.validate import Length, Range
from datetime import datetime

class PostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Post
    
    username = ma.String(required=True, validate=Length(min=4))
    content = ma.String(required=True)
    likes = ma.Integer(required=True, validate=Range(min=0))
    last_updated = ma.DateTime(required=True,nullable=False, default=datetime.utcnow)


post_schema = PostSchema()
post_schemas = PostSchema(many=True)