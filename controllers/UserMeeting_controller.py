from schemas.UserMeetingSchema import user_meeting_schema
from schemas.UserMeetingSchema import user_meeting_schemas
from models.User import User
from models.UserMeeting import UserMeeting

from main import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify, abort
from sqlalchemy.orm import joinedload


usermeeting = Blueprint('usermeeting', __name__, url_prefix="/usermeeting")

@usermeeting.route("/", methods=["GET"])
def usermeeting_all():
    # Retrieve all workhistorys
    user_certifications = UserMeeting.query.all()
    return jsonify(user_meeting_schemas.dump(user_certifications))


@usermeeting.route("/<string:inputted_username>", methods=["GET"])
def usermeeting_user(inputted_username):
    # Retrieve a particular users workhistorys

    user_object = User.query.get(inputted_username)

    if not user_object:
        return abort(401, description="Invalid user")

    user_meeting_unordered = UserMeeting.query.filter_by(username=inputted_username)

    if not user_meeting_unordered:
        return abort(404, description="No work histories to return")

    user_meeting_ordered = user_meeting_unordered.order_by(UserMeeting.date_start.desc()).all()
    return jsonify(user_meeting_schemas.dump(user_meeting_ordered))


@usermeeting.route("/", methods=["POST"])
@jwt_required
def usermeeting_create():

    user_meeting_inputted_fields = user_meeting_schema.load(request.json)
    username_of_jwt = get_jwt_identity()

    user_of_jwt = User.query.get(username_of_jwt)

    if not user_of_jwt:
        return abort(404, description="User does not exist")


    # user_id = get_jwt_identity()
    user_meeting_object_from_fields = UserMeeting()

    user_meeting_object_from_fields.username = username_of_jwt
    user_meeting_object_from_fields.time_start = user_meeting_inputted_fields["time_start"]
    user_meeting_object_from_fields.time_end = user_meeting_inputted_fields["time_end"]
    user_meeting_object_from_fields.location = user_meeting_inputted_fields["location"]
    user_meeting_object_from_fields.subject = user_meeting_inputted_fields["subject"]
    user_meeting_object_from_fields.description = user_meeting_inputted_fields["description"]
    user_meeting_object_from_fields.last_updated = user_meeting_inputted_fields["last_updated"]

    db.session.add(user_meeting_object_from_fields)
    
    db.session.commit()

    return jsonify(user_meeting_schema.dump(user_meeting_object_from_fields))


@usermeeting.route("/<int:id>", methods=["GET"])
def usermeeting_get(id):
    #Return a single work history
    user_meeting_object = UserMeeting.query.get(id)
    return jsonify(user_meeting_schema.dump(user_meeting_object))

@usermeeting.route("/<int:id>", methods=["PUT", "PATCH"])
@jwt_required
def usermeeting_update(id):

    jwt_username = get_jwt_identity()

    user_meeting_fields = user_meeting_schema.load(request.json, partial=True)

    jwt_user = User.query.get(jwt_username)

    if not jwt_user:
        return abort(401, description="Invalid user")

    user_meeting_object = UserMeeting.query.filter_by(id=id, username=jwt_username)

    if user_meeting_object.count() != 1:
        return abort(401, description="Unauthorised to update this profile")

    user_meeting_object.update(user_meeting_fields)
    db.session.commit()

    return jsonify(user_meeting_schema.dump(user_meeting_object[0]))



@usermeeting.route("/<int:id>", methods=["DELETE"])
@jwt_required
def usermeeting_delete(id):

    #Delete a work history

    jwt_username = get_jwt_identity()

    user_meeting_object = UserMeeting.query.filter_by(id=id).first()

    if user_meeting_object is None:
        return abort(401, description=f"There does not exist a usercertification with id {id}")


    if (jwt_username != user_meeting_object.username):
        return abort(401, description=f"You are logged in as username: {jwt_username} but the usercertification id matches to {user_meeting_object.username} ")

    # Check the user that wants to delete the workhistory

    user_meeting_object = UserMeeting.query.filter_by(id=id, username=jwt_username).first()

    if not user_meeting_object:
        return abort(401, description=f"usercertification Id of {id} does not exist for this user.")

    db.session.delete(user_meeting_object)

    json_object_to_return = jsonify(user_meeting_schema.dump(user_meeting_object))

    db.session.commit()

    return json_object_to_return


