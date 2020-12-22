
from schemas.UserStudyHistorySchema import user_study_history_schema
from schemas.UserStudyHistorySchema import user_study_history_schemas
from models.User import User
from models.UserStudyHistory import UserStudyHistory

from main import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify, abort
from sqlalchemy.orm import joinedload
userstudyhistory = Blueprint('userstudyhistory', __name__, url_prefix="/userstudyhistory")

@userstudyhistory.route("/", methods=["GET"])
def userStudyhistory_all():
    # Retrieve all Studyhistorys
    user_study_histories = UserStudyHistory.query.all()
    return jsonify(user_study_history_schemas.dump(user_study_histories))


@userstudyhistory.route("/user/<string:inputted_username>", methods=["GET"])
def userStudyhistory_user(inputted_username):
    # Retrieve a particular users Studyhistorys

    user_object = User.query.get(inputted_username)

    if not user_object:
        return abort(401, description="Invalid user")

    user_study_histories_unordered = UserStudyHistory.query.filter_by(username=inputted_username)

    if not user_study_histories_unordered:
        return abort(404, description="No Study histories to return")

    user_study_histories_ordered = user_study_histories_unordered.order_by(UserStudyHistory.date_start.desc()).all()
    return jsonify(user_study_history_schemas.dump(user_study_histories_ordered))


@userstudyhistory.route("/user/", methods=["POST"])
@jwt_required
def userStudyhistory_create():

    user_study_history_inputted_fields = user_study_history_schema.load(request.json)

    username_of_jwt = get_jwt_identity()

    user_of_jwt = User.query.get(username_of_jwt)

    if not user_of_jwt:
        return abort(404, description="User does not exist")



    # user_id = get_jwt_identity()
    user_study_history_object_from_fields = UserStudyHistory()

    user_study_history_object_from_fields.qualification_title = user_study_history_inputted_fields["qualification_title"]
    user_study_history_object_from_fields.institution = user_study_history_inputted_fields["institution"]
    user_study_history_object_from_fields.city = user_study_history_inputted_fields["city"]
    user_study_history_object_from_fields.country = user_study_history_inputted_fields["country"]
    user_study_history_object_from_fields.date_start = user_study_history_inputted_fields["date_start"]
    user_study_history_object_from_fields.date_end = user_study_history_inputted_fields["date_end"]
    user_study_history_object_from_fields.last_updated = user_study_history_inputted_fields["last_updated"]

    db.session.add(user_study_history_object_from_fields)
    
    db.session.commit()

    return jsonify(user_study_history_schema.dump(user_study_history_object_from_fields))


@userstudyhistory.route("/<int:id>", methods=["GET"])
def userStudyhistory_get(id):
    #Return a single Study history
    user_study_history_object = UserStudyHistory.query.get(id)
    return jsonify(user_study_history_schema.dump(user_study_history_object))

@userstudyhistory.route("/user/<int:id>", methods=["PUT", "PATCH"])
@jwt_required
def userStudyhistory_update(id):

    jwt_username = get_jwt_identity()

    user_study_history_fields = user_study_history_schema.load(request.json, partial=True)

    jwt_user = User.query.get(jwt_username)

    if not jwt_user:
        return abort(401, description="Invalid user")

    user_study_history_object = UserStudyHistory.query.filter_by(id=id, username=jwt_username)

    if user_study_history_object.count() != 1:
        return abort(401, description="Unauthorised to update this profile")

    user_study_history_object.update(user_study_history_fields)
    db.session.commit()

    return jsonify(user_study_history_schema.dump(user_study_history_object[0]))



@userstudyhistory.route("/<int:id>", methods=["DELETE"])
@jwt_required
def userStudyhistory_delete(id):

    #Delete a Study history

    jwt_username = get_jwt_identity()

    user_study_history_object = UserStudyHistory.query.filter_by(id=id).first()

    if user_study_history_object is None:
        return abort(401, description=f"There does not exist a Studyhistory with id {id}")


    if (jwt_username != user_study_history_object.username):
        return abort(401, description=f"You are logged in as username: {jwt_username} but the study history id matches to {user_study_history_object.username} ")

    # Check the user that wants to delete the Studyhistory
    user_study_history_object = UserStudyHistory.query.filter_by(id=id, username=jwt_username).first()

    if not user_study_history_object:
        return abort(401, description=f"Study history Id of {id} does not exist for this user.")

    db.session.delete(user_study_history_object)
    db.session.commit()

    return jsonify(user_study_history_schema.dump(user_study_history_object))


