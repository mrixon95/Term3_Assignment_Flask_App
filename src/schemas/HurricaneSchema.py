from main import ma
from models.Hurricane import Hurricane
from marshmallow.validate import Length

class HurricaneSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Hurricane

    name = ma.String(required=True, validate=Length(min=1))
    size = ma.String(required=True, validate=Length(min=1))

book_image_schema = HurricaneSchema()