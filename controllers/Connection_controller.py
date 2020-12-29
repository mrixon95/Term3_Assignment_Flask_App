from schemas.ConnectionSchema import connection_schema
from schemas.ConnectionSchema import connection_schemas
from models.User import User
from models.Connection import Connection

from main import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify, abort
from sqlalchemy.orm import joinedload
from datetime import datetime


connection = Blueprint('connection', __name__, url_prefix="/connection")


@connection.route("/all", methods=["GET"])
def get_all_connections():
    # Retrieve all workhistorys
    connections = Connection.query.all()
    return jsonify(connection_schemas.dump(connections))


@connection.route("/<string:username>", methods=["GET"])
def get_individual_users_connections(username):

    user_inputted = User.query.get(username)

    if not user_inputted:
        return abort(404, description="User does not exist")

    connections = Connection.query.filter(
        ((Connection.username_of_requester == username) | (Connection.username_of_confirmer == username))
        & (Connection.status == "confirmed")).all()

    return jsonify(connection_schemas.dump(connections))

@connection.route("/pending/<string:username>", methods=["GET"])
def get_individual_users_pending_connections(username):

    user_inputted = User.query.get(username)

    if not user_inputted:
        return abort(404, description="User does not exist")

    connections = Connection.query.filter(
        ((Connection.username_of_requester == username) | (Connection.username_of_confirmer == username))
        & (Connection.status == "pending")).all()

    return jsonify(connection_schemas.dump(connections))


@connection.route("/<string:otheruser>", methods=["POST"])
@jwt_required
def create_new_connection(otheruser):

    jwt_username = get_jwt_identity()
    other_user_object = User.query.filter_by(username = otheruser)

    if not other_user_object:
        return abort(401, description=f"User {otheruser} does not exist")

    connection_object = Connection.query.filter(
        Connection.username_of_requester.in_([jwt_username, otheruser]) &
        Connection.username_of_confirmer.in_([jwt_username, otheruser])
        ).first()

    if connection_object:
        return abort(401, description=f"A connection between users {jwt_username} and {otheruser} already exists")

    # Connection object should be between the user making the request and the other user

    new_connection_object = Connection()

    new_connection_object.username_of_requester = jwt_username
    new_connection_object.username_of_confirmer = otheruser


    db.session.add(new_connection_object)
    
    db.session.commit() 

    return jsonify(connection_schema.dump(new_connection_object))


@connection.route("/confirm/<string:otheruser>", methods=["PUT"])
@jwt_required
def confirm_connection(otheruser):

    username_of_jwt = get_jwt_identity()
    other_user_object = User.query.filter_by(username = otheruser)

    if not other_user_object:
        return abort(401, description=f"User {otheruser} does not exist")

     # user_id = get_jwt_identity()


    connection_object = Connection.query.filter(
        (Connection.username_of_requester == otheruser) &
        (Connection.username_of_confirmer == username_of_jwt)
        ).first()

    if connection_object.status == "confirmed":
        return abort(401, description=f"Connection between {username_of_jwt} and {otheruser} is already confirmed")

    if connection_object is None:
        return abort(401, description=f"Could not find connection request from {username_of_jwt} to {otheruser}")   

    connection_object.user_2_approved = True
    connection_object.status = "confirmed"
    
    db.session.commit() 

    return jsonify(connection_schema.dump(connection_object))



@connection.route("/<string:otheruser>", methods=["DELETE"])
@jwt_required
def delete_connection(otheruser):

    # Delete a connection

    jwt_username = get_jwt_identity()

    # Connection object should be between the user making the request and the other user

    connection_object = Connection.query.filter(
        Connection.username_of_requester.in_([jwt_username, otheruser]) &
        Connection.username_of_confirmer.in_([jwt_username, otheruser])
        ).first()

    if connection_object is None:
        return abort(401, description=f"There does not exist a connection between {jwt_username} and {otheruser}")

    json_object_to_return = jsonify(connection_schema.dump(connection_object))

    db.session.delete(connection_object)

    db.session.commit()

    return json_object_to_return




# @connection.route("/", methods=["POST"])
# @jwt_required
# def message_create():
#     # Retrieve a particular users workhistorys

#     username_of_jwt = get_jwt_identity()
#     user_sender_object = User.query.get(username_of_jwt)
#     user_receiver_object = User.query.get(request.json["username_of_receiver"])

#     if not (user_sender_object or user_receiver_object):
#         return abort(401, description="A user is invalid")

#     if not request.json["content"]:
#         return abort(401, description="Must have non-empty content")

#      # user_id = get_jwt_identity()
#     message_object_from_fields = Message()

#     message_object_from_fields.username_of_sender = username_of_jwt
#     message_object_from_fields.username_of_receiver = request.json["username_of_receiver"]
#     message_object_from_fields.content = request.json["content"]

#     db.session.add(message_object_from_fields)
    
#     db.session.commit() 
#     return jsonify(message_schema.dump(message_object_from_fields))


# @message.route("/betweentwousers", methods=["GET"])
# @jwt_required
# def see_discussion_between_two_users():

#     username_of_jwt = get_jwt_identity()
#     other_user_username = request.json["other_user"]

#     user_of_jwt_object = User.query.get(username_of_jwt)
#     other_user_object = User.query.get(other_user_username)

#     if not (user_of_jwt_object or other_user_object):
#         return abort(401, description="One or both users are invalid")

#     messages = Message.query.filter(Message.username_of_sender.in_([username_of_jwt, other_user_username]) & Message.username_of_receiver.in_([username_of_jwt, other_user_username])).all()


#     return jsonify(message_schemas.dump(messages))


# @message.route("/read/<int:id>", methods=["GET"])
# @jwt_required
# def read_message_using_id(id):
#     #Return a single work history
#     message_object = Message.query.get(id)
#     username_of_jwt = get_jwt_identity()
#     print(message_object.username_of_sender)
#     print(message_object.username_of_receiver)
#     print(username_of_jwt)
#     if (message_object.username_of_sender == username_of_jwt or message_object.username_of_receiver == username_of_jwt):
#         if (message_object.username_of_receiver == username_of_jwt):
#             message_object.read = True
#             db.session.commit()
#             # reading a message only makes sense when it is the receiver who gets it
        
#         return jsonify(message_schema.dump(message_object))

#     return abort(401, description=f"Message with id {id} and a user with username {username_of_jwt} cannot be found")

# @message.route("/like/<int:id>", methods=["POST"])
# @jwt_required
# def like_message_using_id(id):
#     #Return a single work history
#     message_object = Message.query.get(id)
#     username_of_jwt = get_jwt_identity()
#     print(username_of_jwt)
#     print(message_object.username_of_receiver)
    
#     if (message_object.username_of_receiver == username_of_jwt):
#         print(message_object.liked)
#         message_object.liked = True
#         db.session.commit()
#         return "Message was liked."
#             # reading a message only makes sense when it is the receiver who gets it

#     return abort(401, description=f"Message with id {id} and a user with username {username_of_jwt} cannot be liked")

