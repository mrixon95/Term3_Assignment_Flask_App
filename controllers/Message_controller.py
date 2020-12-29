from schemas.MessageSchema import message_schema
from schemas.MessageSchema import message_schemas
from models.User import User
from models.Message import Message

from main import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify, abort
from sqlalchemy.orm import joinedload
from datetime import datetime


message = Blueprint('message', __name__, url_prefix="/message")


@message.route("/all", methods=["GET"])
def get_all_messages():
    # Retrieve all workhistorys
    messages = Message.query.all()
    return jsonify(message_schemas.dump(messages))


@message.route("/singleuser", methods=["GET"])
@jwt_required
def get_personal_messages():

    username_of_jwt = get_jwt_identity()

    user_of_jwt = User.query.get(username_of_jwt)

    if not user_of_jwt:
        return abort(404, description="User does not exist")

    messages = Message.query.filter((Message.username_of_sender == username_of_jwt) | (Message.username_of_receiver == username_of_jwt) ).all()

    return jsonify(message_schemas.dump(messages))


@message.route("/", methods=["POST"])
@jwt_required
def message_create():
    # Retrieve a particular users workhistorys

    username_of_jwt = get_jwt_identity()
    user_sender_object = User.query.get(username_of_jwt)
    user_receiver_object = User.query.get(request.json["username_of_receiver"])

    if not (user_sender_object or user_receiver_object):
        return abort(401, description="A user is invalid")

    if not request.json["content"]:
        return abort(401, description="Must have non-empty content")

     # user_id = get_jwt_identity()
    message_object_from_fields = Message()

    message_object_from_fields.username_of_sender = username_of_jwt
    message_object_from_fields.username_of_receiver = request.json["username_of_receiver"]
    message_object_from_fields.content = request.json["content"]

    db.session.add(message_object_from_fields)
    
    db.session.commit() 
    return jsonify(message_schema.dump(message_object_from_fields))


@message.route("/betweentwousers", methods=["GET"])
@jwt_required
def see_discussion_between_two_users():

    username_of_jwt = get_jwt_identity()
    other_user_username = request.json["other_user"]

    user_of_jwt_object = User.query.get(username_of_jwt)
    other_user_object = User.query.get(other_user_username)

    if not (user_of_jwt_object or other_user_object):
        return abort(401, description="One or both users are invalid")

    messages = Message.query.filter(Message.username_of_sender.in_([username_of_jwt, other_user_username]) & Message.username_of_receiver.in_([username_of_jwt, other_user_username])).all()


    return jsonify(message_schemas.dump(messages))


@message.route("/read/<int:id>", methods=["GET"])
@jwt_required
def read_message_using_id(id):
    #Return a single work history
    
    message_object = Message.query.get(id)
    username_of_jwt = get_jwt_identity()
    print(message_object.username_of_sender)
    print(message_object.username_of_receiver)
    print(username_of_jwt)
    if (message_object.username_of_sender == username_of_jwt or message_object.username_of_receiver == username_of_jwt):
        if (message_object.username_of_receiver == username_of_jwt):
            message_object.read = True
            db.session.commit()
            # reading a message only makes sense when it is the receiver who gets it
        
        return jsonify(message_schema.dump(message_object))

    return abort(401, description=f"Message with id {id} and a user with username {username_of_jwt} cannot be found")

@message.route("/like/<int:id>", methods=["POST"])
@jwt_required
def like_message_using_id(id):
    #Return a single work history
    message_object = Message.query.get(id)
    username_of_jwt = get_jwt_identity()
    print(username_of_jwt)
    print(message_object.username_of_receiver)
    
    if (message_object.username_of_receiver == username_of_jwt):
        print(message_object.liked)
        message_object.liked = True
        db.session.commit()
        return "Message was liked."
            # reading a message only makes sense when it is the receiver who gets it

    return abort(401, description=f"Message with id {id} and a user with username {username_of_jwt} cannot be liked")




# @message.route("/<int:id>", methods=["GET"])
# def message_get(id):
#     #Return a single work history
#     user_meeting_object = UserMeeting.query.get(id)
#     return jsonify(user_meeting_schema.dump(user_meeting_object))


# @message.route("/<int:id>", methods=["PUT", "PATCH"])
# @jwt_required
# def message_update(id):

#     jwt_username = get_jwt_identity()

#     user_meeting_fields = user_meeting_schema.load(request.json, partial=True)

#     jwt_user = User.query.get(jwt_username)

#     if not jwt_user:
#         return abort(401, description="Invalid user")

#     user_meeting_object = UserMeeting.query.filter_by(id=id, username=jwt_username)

#     if user_meeting_object.count() != 1:
#         return abort(401, description="Unauthorised to update this profile")

#     user_meeting_object.update(user_meeting_fields)
#     db.session.commit()

#     return jsonify(user_meeting_schema.dump(user_meeting_object[0]))



# @message.route("/<int:id>", methods=["DELETE"])
# @jwt_required
# def message_delete(id):

#     #Delete a work history

#     jwt_username = get_jwt_identity()

#     user_meeting_object = UserMeeting.query.filter_by(id=id).first()

#     if user_meeting_object is None:
#         return abort(401, description=f"There does not exist a usercertification with id {id}")


#     if (jwt_username != user_meeting_object.username):
#         return abort(401, description=f"You are logged in as username: {jwt_username} but the usercertification id matches to {user_meeting_object.username} ")

#     # Check the user that wants to delete the workhistory

#     user_meeting_object = UserMeeting.query.filter_by(id=id, username=jwt_username).first()

#     if not user_meeting_object:
#         return abort(401, description=f"usercertification Id of {id} does not exist for this user.")

#     db.session.delete(user_meeting_object)

#     json_object_to_return = jsonify(user_meeting_schema.dump(user_meeting_object))

#     db.session.commit()

#     return json_object_to_return


