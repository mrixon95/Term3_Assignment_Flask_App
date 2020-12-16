from models.BookImage import BookImage
from models.Book import Book
from schemas.BookImageSchema import book_image_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify, abort, current_app, Response
import boto3
from main import db
from pathlib import Path

book_images = Blueprint('book_images', __name__, url_prefix="/books/<int:book_id>/image")

@book_images.route("/", methods=["POST"])
@jwt_required
def book_image_create(book_id):
    books = Book.query.filter_by(id=book_id, user_id=get_jwt_identity())

    if books.count() != 1:
        return abort(401, description="Invalid book")

    if "image" not in request.files:
        return abort(400, description="No image")
        
    image = request.files["image"]

    # if Path(image.filename).suffix != ".png":
    #     return abort(400, description="Invalid file type")

    filename = f"{book_id}.png"
    bucket = boto3.resource("s3").Bucket(current_app.config["AWS_S3_BUCKET"])
    key = f"book_images/{filename}"
    bucket.upload_fileobj(image, key)

    if not(books[0].book_image):
        new_image = BookImage()
        new_image.filename = filename 
        books[0].book_image = new_image
        db.session.commit()
        
    return ("", 200)


@book_images.route("/<int:id>", methods=["GET"])
def book_image_show(book_id, id):
    book_image = BookImage.query.filter_by(id=id, book_id=book_id).first()

    if not book_image:
        return abort(404, description="No book image")
    
    bucket = boto3.resource("s3").Bucket(current_app.config["AWS_S3_BUCKET"])
    filename = book_image.filename
    file_obj = bucket.Object(f"book_images/{filename}").get()

    return Response(
        file_obj['Body'].read(),
        mimetype='image/png',
        headers={"Content-Disposition": f"attachment;filename=image"}
    )

@book_images.route("/<int:id>", methods=["DELETE"])
@jwt_required
def book_image_delete(book_id, id):
    book = Book.query.filter_by(id=book_id, user_id=get_jwt_identity()).first()

    if not book:
        return abort(401, description="Invalid book")
    
    if book.book_image:
        bucket = boto3.resource("s3").Bucket(current_app.config["AWS_S3_BUCKET"])
        filename = book.book_image.filename

        bucket.Object(f"book_images/{filename}").delete()
        
        db.session.delete(book.book_image)
        db.session.commit()

    return jsonify("successfully removed")