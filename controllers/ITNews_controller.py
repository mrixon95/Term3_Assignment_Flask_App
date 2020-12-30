
from schemas.ITNewsSchema import IT_news_schema
from schemas.ITNewsSchema import IT_news_schemas
from models.User import User
from models.ITNews import ITNews

from main import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify, abort
from sqlalchemy.orm import joinedload
itnews = Blueprint('itnews', __name__, url_prefix="/itnews")

@itnews.route("/", methods=["GET"])
def itnews_all():
    # Retrieve all workhistorys
    it_news = ITNews.query.all()
    return jsonify(IT_news_schemas.dump(it_news))


@itnews.route("/", methods=["POST"])
def itnews_create():

    it_news_object = IT_news_schemas.load(request.json)

    db.session.add(it_news_object)
    
    db.session.commit()

    return jsonify(IT_news_schema.dump(it_news_object))


@itnews.route("/<int:id>", methods=["GET"])
def itnews_get(id):
    #Return a single work history
    it_news_object = ITNews.query.get(id)
    return jsonify(IT_news_schema.dump(it_news_object))


@itnews.route("/<int:id>", methods=["PUT", "PATCH"])
def itnews_update(id):

    it_news_fields = IT_news_schema.load(request.json, partial=True)

    it_news_object = ITNews.query.filter_by(id=id)

    if it_news_object.count() != 1:
        return abort(401, description=f"Job salary with id {id} does not exist")

    it_news_object.update(it_news_fields)
    db.session.commit()

    return jsonify(IT_news_schema.dump(it_news_object[0]))



@itnews.route("/<int:id>", methods=["DELETE"])
def itnews_delete(id):

    #Delete a work history

    it_news_object = ITNews.query.filter_by(id=id).first()

    if it_news_object is None:
        return abort(401, description=f"There does not exist an it news object with id {id}")


    json_object_to_return = jsonify(IT_news_schema.dump(it_news_object))

    db.session.delete(it_news_object)

    db.session.commit()

    return json_object_to_return




