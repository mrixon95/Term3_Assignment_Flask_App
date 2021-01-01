from schemas.UserSchema import user_schema
from schemas.UserSchema import user_schemas
from main import bcrypt
from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import create_access_token

from models.User import User

from main import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify, abort
from sqlalchemy.orm import joinedload
from datetime import timedelta
user = Blueprint('user', __name__, url_prefix="/user")

@user.route("/", methods=["GET"])
def user_index():
    # Retrieve all users
    users = User.query.all()
    return jsonify(user_schemas.dump(users))

@user.route("/<string:username_inputted>", methods=["GET"])
def user_get(username_inputted):
    #Return a single Study history
    user_object = User.query.filter_by(username=username_inputted).first()
    if not user_object:
        return abort(401, description="Invalid id for a user")
        
    return jsonify(user_schema.dump(user_object))


@user.route("/", methods=["POST"])
def user_create():

    user_fields = user_schema.load(request.json)

    user_with_same_email = User.query.filter_by(email=user_fields["email"]).first()
    user_with_same_username = User.query.filter_by(username=user_fields["username"]).first()

    if user_with_same_email:
         return abort(400, description="Username already registered")

    if user_with_same_username:
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



@user.route("/login", methods=["POST"])
def user_login():

    username_submitted = request.json["username"]
    password_submitted = request.json["password"]

    print("username_submitted: " + username_submitted)
    print("password_submitted: " + password_submitted)
    user = User.query.filter_by(username=username_submitted).first()

    if not user or not bcrypt.check_password_hash(user.password, password_submitted):
        return abort(401, description="Incorrect username and password")
    
    expiry = timedelta(days=1)
    access_token = create_access_token(identity=str(user.username), expires_delta=expiry)

    return jsonify({ "token": access_token })



@user.route("/<int:id>", methods=["GET"])
def book_show(id):
    #Return a single book
    # book = Book.query.get(id)
    # return jsonify(book_schema.dump(book))
    pass

@user.route("/<int:id>", methods=["PUT", "PATCH"])
@jwt_required
def userstudyhistory_update(id):
    #Update a book
    # book_fields = book_schema.load(request.json)
    # user_id = get_jwt_identity()

    # user = User.query.get(user_id)

    # if not user:
    #     return abort(401, description="Invalid user")

    # books = Book.query.filter_by(id=id, user_id=user.id)
    
    # if books.count() != 1:
    #     return abort(401, description="Unauthorized to update this book")

    # books.update(book_fields)
    # db.session.commit()

    # return jsonify(book_schema.dump(books[0]))
    pass

@user.route("/<int:id>", methods=["DELETE"])
@jwt_required
def userstudyhistory_delete(id):
    #Delete a book
    # user_id = get_jwt_identity()

    # user = User.query.get(user_id)

    # if not user:
    #     return abort(401, description="Invalid user")


    # book = Book.query.filter_by(id=id, user_id=user.id).first()

    # if not book:
    #     return abort(400)

    # db.session.delete(book)
    # db.session.commit()

    # return jsonify(book_schema.dump(book))
    pass