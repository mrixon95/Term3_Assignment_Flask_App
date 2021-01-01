from main import ma
from models.ITNews import ITNews
from marshmallow.validate import Length
from datetime import datetime

class ITNewsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ITNews
    
    article_link = ma.Url(required=True)
    photo_link = ma.Url(required=True)
    published_time = ma.DateTime(required=True,nullable=False, default=datetime.utcnow)
    last_updated = ma.DateTime(required=True,nullable=False, default=datetime.utcnow)


IT_news_schema = ITNewsSchema()
IT_news_schemas = ITNewsSchema(many=True)