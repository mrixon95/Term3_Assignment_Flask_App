from main import ma
from models.Comment import Comment
from schemas.ConnectionSchema import ConnectionSchema
from marshmallow.validate import Length

class CommentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Comment

    post_id = ma.String(required=True, validate=Length(min=1))
    username_of_commenter = ma.String(required=True, validate=Length(min=1))
    last_updated = ma.String(required=True, validate=Length(min=4))

connection_schema = ConnectionSchema()
connections_schema = ConnectionSchema(many=True)