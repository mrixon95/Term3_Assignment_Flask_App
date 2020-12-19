from models.User import User
from main import db
from schemas.UserSchema import user_schema

from main import bcrypt
from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import create_access_token
from datetime import timedelta

auth = Blueprint('auth', __name__, url_prefix="/auth")

@auth.route("/register", methods=["POST"])
def auth_register():

    user_fields = user_schema.load(request.json)

    user = User.query.filter_by(email=user_fields["username"]).first()

    if user:
         return abort(400, description="Email already registered")

    user = User()
    user.username = user_fields["username"]
    user.first_name = user_fields["first_name"]
    user.last_name = user_fields["last_name"]
    user.created_at = user_fields["created_at"]
    user.dob = user_fields["dob"]
    user.email = user_fields["email"]
    user.mobile = user_fields["mobile"]
    user.city = user_fields["city"]
    user.country = user_fields["country"]
    user.password = bcrypt.generate_password_hash(user_fields["password"]).decode("utf-8")

    db.session.add(user)
    db.session.commit()

    return jsonify(user_schema.dump(user))


@auth.route("/login", methods=["POST"])
def auth_login():

    username_submitted = request.json.get("username")
    password_submitted = request.json.get("password")

    user = User.query.filter_by(username=username_submitted).first()

    if not user or not bcrypt.check_password_hash(user.password, password_submitted):
        return abort(401, description="Incorrect username and password")
    
    expiry = timedelta(days=1)
    access_token = create_access_token(identity=str(user.username), expires_delta=expiry)

    return jsonify({ "token": access_token })