from models.User import User
from schemas.UserSchema import user_schema, user_schemas
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify, abort, current_app, Response, render_template
import boto3
from main import db
from pathlib import Path
from services.auth_service import verify_user

book_web = Blueprint('book_web', __name__, url_prefix="/book_web")

@book_web.route("/", methods=["GET"])
def book_web_index():
    # Retrieve all books
    users = User.query.all()
    # return jsonify(books_schema.dump(books))
    # return jsonify(user_schemas.dump(users))
    return render_template("books_index.html", users=users)