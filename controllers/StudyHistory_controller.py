
from schemas.StudyHistorySchema import study_history_schema
from schemas.StudyHistorySchema import study_history_schemas
from models.User import User
from models.StudyHistory import StudyHistory

from main import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify, abort
from sqlalchemy.orm import joinedload
studyhistory = Blueprint('studyhistory', __name__, url_prefix="/studyhistory")

@studyhistory.route("/", methods=["GET"])
def studyhistory_all():
    # Retrieve all Studyhistorys
    study_histories = StudyHistory.query.all()
    return jsonify(study_history_schemas.dump(study_histories))


@studyhistory.route("/user/<string:inputted_username>", methods=["GET"])
def studyhistory_user(inputted_username):
    # Retrieve a particular users Studyhistorys

    user_object = User.query.get(inputted_username)

    if not user_object:
        return abort(401, description="Invalid user")

    study_histories_unordered = StudyHistory.query.filter_by(username=inputted_username)

    if not study_histories_unordered:
        return abort(404, description="No Study histories to return")

    study_histories_ordered = study_histories_unordered.order_by(StudyHistory.date_start.desc()).all()
    return jsonify(study_history_schemas.dump(study_histories_ordered))


@studyhistory.route("/", methods=["POST"])
@jwt_required
def studyhistory_create():

    study_history_inputted_fields = study_history_schema.load(request.json)

    username_of_jwt = get_jwt_identity()

    user_of_jwt = User.query.get(username_of_jwt)

    if not user_of_jwt:
        return abort(404, description="User does not exist")



    # user_id = get_jwt_identity()
    study_history_object_from_fields = StudyHistory()

    study_history_object_from_fields.qualification_title = study_history_inputted_fields["qualification_title"]
    study_history_object_from_fields.institution = study_history_inputted_fields["institution"]
    study_history_object_from_fields.city = study_history_inputted_fields["city"]
    study_history_object_from_fields.country = study_history_inputted_fields["country"]
    study_history_object_from_fields.date_start = study_history_inputted_fields["date_start"]
    study_history_object_from_fields.date_end = study_history_inputted_fields["date_end"]
    study_history_object_from_fields.last_updated = study_history_inputted_fields["last_updated"]
    study_history_object_from_fields.username = username_of_jwt

    db.session.add(study_history_object_from_fields)
    
    db.session.commit()

    return jsonify(study_history_schema.dump(study_history_object_from_fields))


@studyhistory.route("/<int:id>", methods=["GET"])
def studyhistory_get(id):
    #Return a single Study history
    study_history_object = StudyHistory.query.get(id)
    return jsonify(study_history_schema.dump(study_history_object))

@studyhistory.route("/<int:id>", methods=["PUT", "PATCH"])
@jwt_required
def studyhistory_update(id):

    jwt_username = get_jwt_identity()

    study_history_fields = study_history_schema.load(request.json, partial=True)

    jwt_user = User.query.get(jwt_username)

    if not jwt_user:
        return abort(401, description="Invalid user")

    study_history_object = StudyHistory.query.filter_by(id=id, username=jwt_username)

    if study_history_object.count() != 1:
        return abort(401, description="Unauthorised to update this profile")

    study_history_object.update(study_history_fields)
    db.session.commit()

    return jsonify(study_history_schema.dump(study_history_object[0]))



@studyhistory.route("/<int:id>", methods=["DELETE"])
@jwt_required
def studyhistory_delete(id):

    #Delete a Study history

    jwt_username = get_jwt_identity()

    study_history_object = StudyHistory.query.filter_by(id=id).first()

    if study_history_object is None:
        return abort(401, description=f"There does not exist a Studyhistory with id {id}")


    if (jwt_username != study_history_object.username):
        return abort(401, description=f"You are logged in as username: {jwt_username} but the study history id matches to {study_history_object.username} ")

    # Check the user that wants to delete the Studyhistory
    study_history_object = StudyHistory.query.filter_by(id=id, username=jwt_username).first()

    if not study_history_object:
        return abort(401, description=f"Study history Id of {id} does not exist for this user.")

    db.session.delete(study_history_object)

    json_object_to_return = jsonify(study_history_schema.dump(study_history_object))

    db.session.commit()

    return json_object_to_return



