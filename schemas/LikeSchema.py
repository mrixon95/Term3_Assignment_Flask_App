from main import ma

from schemas.PostSchema import post_schema
from schemas.UserSchema import user_schema
from models.Likes_Table import Likes_Table
from marshmallow.validate import Length, OneOf
from datetime import datetime

class LikeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Likes_Table

    post = ma.Nested(post_schema)
    user = ma.Nested(user_schema)

like_schema = LikeSchema()
like_schemas = LikeSchema(many=True)