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
    for message in messages:
        print(message.sender)
        print(message.username_of_receiver)
    return jsonify(message_schemas.dump(messages))


@message.route("/", methods=["GET"])
@jwt_required
def get_personal_messages():

    username_of_jwt = get_jwt_identity()
    print(username_of_jwt)
    user_of_jwt = User.query.get(username_of_jwt)
    print(user_of_jwt)

    if not user_of_jwt:
        return abort(404, description="User does not exist")

    messages = Message.query.filter_by(username_from=username_of_jwt)

    return jsonify(message_schemas.dump(messages))


@message.route("/", methods=["POST"])
@jwt_required
def message_create():
    # Retrieve a particular users workhistorys

    username_of_jwt = get_jwt_identity()
    user_object = User.query.get(username_of_jwt)

    if not user_object:
        return abort(401, description="Invalid user")

     # user_id = get_jwt_identity()
    message_object_from_fields = Message()

    message_object_from_fields.username_from = username_of_jwt
    message_object_from_fields.username_to = request.json["username_to"]
    message_object_from_fields.content = request.json["content"]

    db.session.add(message_object_from_fields)
    
    db.session.commit() 
    return jsonify(message_schema.dump(message_object_from_fields))


# @message.route("/", methods=["POST"])
# @jwt_required
# def message_create():

#     user_meeting_inputted_fields = user_meeting_schema.load(request.json)
#     username_of_jwt = get_jwt_identity()

#     user_of_jwt = User.query.get(username_of_jwt)

#     if not user_of_jwt:
#         return abort(404, description="User does not exist")


#     # user_id = get_jwt_identity()
#     user_meeting_object_from_fields = UserMeeting()

#     user_meeting_object_from_fields.username = username_of_jwt
#     user_meeting_object_from_fields.time_start = user_meeting_inputted_fields["time_start"]
#     user_meeting_object_from_fields.time_end = user_meeting_inputted_fields["time_end"]
#     user_meeting_object_from_fields.location = user_meeting_inputted_fields["location"]
#     user_meeting_object_from_fields.subject = user_meeting_inputted_fields["subject"]
#     user_meeting_object_from_fields.description = user_meeting_inputted_fields["description"]
#     user_meeting_object_from_fields.last_updated = user_meeting_inputted_fields["last_updated"]

#     db.session.add(user_meeting_object_from_fields)
    
#     db.session.commit()

#     return jsonify(user_meeting_schema.dump(user_meeting_object_from_fields))


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


