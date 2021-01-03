from main import ma


class UserCountSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
    
        username = ma.String(required=True)
        count = ma.Integer(required=True)


user_count_schema = UserCountSchema()
user_count_schemas = UserCountSchema(many=True)