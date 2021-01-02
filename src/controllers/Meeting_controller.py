from schemas.MeetingSchema import meeting_schema
from schemas.MeetingSchema import meeting_schemas
from models.User import User
from models.Meeting import Meeting

from main import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify, abort
from sqlalchemy.orm import joinedload


meeting = Blueprint('meeting', __name__, url_prefix="/meeting")

# @meeting.route("/", methods=["GET"])
# def meeting_all():
#     # Retrieve all workhistorys
#     meetings = Meeting.query.all()
#     return jsonify(meeting_schemas.dump(meetings))


@meeting.route("/<string:inputted_username>", methods=["GET"])
def meeting_user(inputted_username):
    # Retrieve a particular users workhistorys

    user_object = User.query.get(inputted_username)

    if not user_object:
        return abort(401, description="Invalid user")

    meeting_unordered = Meeting.query.filter_by(username=inputted_username)

    if not meeting_unordered:
        return abort(404, description="No work histories to return")

    meeting_ordered = meeting_unordered.order_by(Meeting.date_start.desc()).all()
    return jsonify(meeting_schemas.dump(meeting_ordered))


@meeting.route("/", methods=["POST"])
@jwt_required
def meeting_create():

    meeting_inputted_fields = meeting_schema.load(request.json)
    username_of_jwt = get_jwt_identity()

    user_of_jwt = User.query.get(username_of_jwt)

    if not user_of_jwt:
        return abort(404, description="User does not exist")


    # user_id = get_jwt_identity()
    meeting_object_from_fields = Meeting()

    meeting_object_from_fields.username = username_of_jwt
    meeting_object_from_fields.time_start = meeting_inputted_fields["time_start"]
    meeting_object_from_fields.time_end = meeting_inputted_fields["time_end"]
    meeting_object_from_fields.location = meeting_inputted_fields["location"]
    meeting_object_from_fields.subject = meeting_inputted_fields["subject"]
    meeting_object_from_fields.description = meeting_inputted_fields["description"]
    meeting_object_from_fields.last_updated = meeting_inputted_fields["last_updated"]

    db.session.add(meeting_object_from_fields)
    
    db.session.commit()

    return jsonify(meeting_schema.dump(meeting_object_from_fields))


@meeting.route("/<int:id>", methods=["GET"])
def meeting_get(id):
    #Return a single work history
    meeting_object = Meeting.query.get(id)
    return jsonify(meeting_schema.dump(meeting_object))

@meeting.route("/<int:id>", methods=["PUT", "PATCH"])
@jwt_required
def meeting_update(id):

    jwt_username = get_jwt_identity()

    meeting_fields = meeting_schema.load(request.json, partial=True)

    jwt_user = User.query.get(jwt_username)

    if not jwt_user:
        return abort(401, description="Invalid user")

    meeting_object = Meeting.query.filter_by(id=id, username=jwt_username)

    if meeting_object.count() != 1:
        return abort(401, description="Unauthorised to update this profile")

    meeting_object.update(meeting_fields)
    db.session.commit()

    return jsonify(meeting_schema.dump(meeting_object[0]))



@meeting.route("/<int:id>", methods=["DELETE"])
@jwt_required
def meeting_delete(id):

    #Delete a work history

    jwt_username = get_jwt_identity()

    meeting_object = Meeting.query.filter_by(id=id).first()

    if meeting_object is None:
        return abort(401, description=f"There does not exist a usercertification with id {id}")


    if (jwt_username != meeting_object.username):
        return abort(401, description=f"You are logged in as username: {jwt_username} but the usercertification id matches to {meeting_object.username} ")

    # Check the user that wants to delete the workhistory

    meeting_object = Meeting.query.filter_by(id=id, username=jwt_username).first()

    if not meeting_object:
        return abort(401, description=f"usercertification Id of {id} does not exist for this user.")

    db.session.delete(meeting_object)

    json_object_to_return = jsonify(meeting_schema.dump(meeting_object))

    db.session.commit()

    return json_object_to_return


