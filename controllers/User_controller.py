from schemas.UserSchema import users_schema

from models.User import User

from main import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify, abort
from sqlalchemy.orm import joinedload
user = Blueprint('user', __name__, url_prefix="/users")

@user.route("/", methods=["GET"])
def user_index():
    #Retrieve all books
    users = User.query.all()
    return jsonify(users_schema.dump(users))


@user.route("/", methods=["POST"])
@jwt_required
def book_create():
    #Create a new book
    # book_fields = book_schema.load(request.json)
    # user_id = get_jwt_identity()

    # user = User.query.get(user_id)

    # if not user:
    #     return abort(401, description="Invalid user")

    # new_book = Book()
    # new_book.title = book_fields["title"]

    # user.books.append(new_book)
    
    # db.session.commit()
    
    # return jsonify(book_schema.dump(new_book))
    pass

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