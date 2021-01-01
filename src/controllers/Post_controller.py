
from schemas.PostSchema import post_schema
from schemas.PostSchema import post_schemas
from models.User import User
from models.Post import Post
from models.Likes_Table import Likes_Table

from schemas.LikeSchema import like_schema
from schemas.LikeSchema import like_schemas

from main import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify, abort
from sqlalchemy.orm import joinedload
post = Blueprint('post', __name__, url_prefix="/post")

@post.route("/", methods=["GET"])
def post_all():
    # Retrieve all Studyhistorys
    posts = Post.query.all()
    return jsonify(post_schemas.dump(posts))


@post.route("/<string:inputted_username>", methods=["GET"])
def user_posts_get(inputted_username):
    # Retrieve a particular Post

    user_object = User.query.get(inputted_username)

    if not user_object:
        return abort(401, description="Invalid user")

    posts_unordered = Post.query.filter_by(username=inputted_username)

    if not posts_unordered:
        return abort(404, description="No Study histories to return")

    posts_ordered = posts_unordered.order_by(Post.last_updated.desc()).all()
    return jsonify(post_schemas.dump(posts_ordered))


@post.route("/<int:inputted_id>", methods=["GET"])
def post_id_get(inputted_id):
    # Retrieve a particular Post

    post_retrieved = Post.query.filter_by(id=inputted_id)

    if not post_retrieved:
        return abort(404, description=f"No post with {inputted_id} exists")

    post_retrieved_ordered = post_retrieved.order_by(Post.last_updated.desc()).all()
    return jsonify(post_schemas.dump(post_retrieved_ordered))


@post.route("/get_users_likes/<int:inputted_id>", methods=["GET"])
def post_id_get_likes(inputted_id):

    import json
    post_retrieved = Post.query.filter_by(id=inputted_id)

    if not post_retrieved:
        return abort(404, description=f"No post with {inputted_id} exists")
    
    likes_object = Likes_Table.query.with_entities(
        Likes_Table.username_of_liker
    ).filter_by(post_id=inputted_id).all()

    users = []
    for username in likes_object:
        print(users.append(username))

    return json.dumps(users)



@post.route("/like/<int:inputted_id>", methods=["POST"])
@jwt_required
def post_id_like(inputted_id):

    # Like a particular Post

    username_of_jwt = get_jwt_identity()

    user_of_jwt = User.query.get(username_of_jwt)

    if not user_of_jwt:
        return abort(404, description="User does not exist")

    post_retrieved = Post.query.filter_by(id=inputted_id).first()

    if not post_retrieved:
        return abort(404, description=f"No post with {inputted_id} exists")


    like_object = Likes_Table.query.filter(
        ((Likes_Table.post_id == inputted_id) & (Likes_Table.username_of_liker == username_of_jwt))
    ).first()

    if like_object:
        return abort(404, description=f"Post {inputted_id} has already been liked by user {username_of_jwt}")


    likes_object = Likes_Table()

    likes_object.post_id = inputted_id
    likes_object.username_of_liker = username_of_jwt

    post_retrieved.likes += 1

    db.session.add(likes_object)
    
    db.session.commit()

    return jsonify(post_schema.dump(likes_object))





@post.route("/unlike/<int:inputted_id>", methods=["DELETE"])
@jwt_required
def post_id_unlike(inputted_id):

    # Like a particular Post

    username_of_jwt = get_jwt_identity()

    user_of_jwt = User.query.get(username_of_jwt)

    if not user_of_jwt:
        return abort(404, description="User does not exist")

    post_retrieved = Post.query.filter_by(id=inputted_id).first()

    if not post_retrieved:
        return abort(404, description=f"No post with {inputted_id} exists")


    like_object = Likes_Table.query.filter(
        ((Likes_Table.post_id == inputted_id) & (Likes_Table.username_of_liker == username_of_jwt))
    ).first()

    if like_object is None:
        return abort(404, description=f"Post {inputted_id} has not been liked by user {username_of_jwt}")


    json_object_to_return = jsonify(like_schema.dump(like_object))

    db.session.delete(like_object)

    db.session.commit()

    return json_object_to_return




@post.route("/", methods=["POST"])
@jwt_required
def post_create():

    username_of_jwt = get_jwt_identity()

    user_of_jwt = User.query.get(username_of_jwt)

    if not user_of_jwt:
        return abort(404, description="User does not exist")



    # user_id = get_jwt_identity()
    post_object_from_fields = Post()

    post_object_from_fields.username = username_of_jwt
    post_object_from_fields.content = request.json["content"]

    db.session.add(post_object_from_fields)
    
    db.session.commit()

    return jsonify(post_schema.dump(post_object_from_fields))


@post.route("/<int:id>", methods=["GET"])
def post_get(id):
    #Return a single Study history
    post_object = Post.query.get(id)
    return jsonify(post_schema.dump(post_object))



@post.route("/<int:id>", methods=["PUT", "PATCH"])
@jwt_required
def post_update(id):

    jwt_username = get_jwt_identity()

    post_fields = post_schema.load(request.json, partial=True)

    jwt_user = User.query.get(jwt_username)

    if not jwt_user:
        return abort(401, description="Invalid user")

    post_object = Post.query.filter_by(id=id, username=jwt_username)

    if post_object.count() != 1:
        return abort(401, description=f"Either post id of {id} or the username is wrong")

    post_object.update(post_fields)
    db.session.commit()

    return jsonify(post_schema.dump(post_object[0]))



@post.route("/<int:id>", methods=["DELETE"])
@jwt_required
def post_delete(id):

    #Delete a Study history

    jwt_username = get_jwt_identity()

    post_object = Post.query.filter_by(id=id).first()

    if post_object is None:
        return abort(401, description=f"There does not exist a post with id {id}")


    if (jwt_username != post_object.username):
        return abort(401, description=f"You are logged in as username: {jwt_username} but the Post id matches to user {post_object.username} ")

    # Check the user that wants to delete the Studyhistory
    post_object = Post.query.filter_by(id=id, username=jwt_username).first()

    if not post_object:
        return abort(401, description=f"Post Id of {id} does not exist for this user.")

    db.session.delete(post_object)

    json_object_to_return = jsonify(post_schema.dump(post_object))

    db.session.commit()

    return json_object_to_return



