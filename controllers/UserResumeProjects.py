from schemas.UserStudyHistorySchema import userStudyHistorySchemas
from schemas.UserStudyHistorySchema import userStudyHistorySchema

from models.User import User
from models.UserStudyHistory import UserStudyHistory
from models.UserWorkHistory import UserWorkHistory

from main import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify, abort
from sqlalchemy.orm import joinedload
userstudyhistory = Blueprint('userstudyhistory', __name__, url_prefix="/userstudyhistory")

@userstudyhistory.route("/", methods=["GET"])
def userstudyhistory_all():
    # Retrieve all workhistorys
    userstudyhistorys = UserStudyHistory.query.all()
    return jsonify(userStudyHistorySchemas.dump(userstudyhistorys))


@userstudyhistory.route("/user/<string:user>", methods=["GET"])
def userstudyhistory_user(user):
    # Retrieve a particular users workhistorys

    user_object = User.query.get(user)

    if not user_object:
        return abort(401, description="Invalid user")

    user_study_histories = UserStudyHistory.query.filter_by(username=user)

    if not user_study_histories:
        return abort(404, description="No study histories to return")

    userstudyhistorys = UserStudyHistory.query.filter_by(username=user).order_by(UserStudyHistory.date_start.desc()).all()
    return jsonify(userStudyHistorySchemas.dump(userstudyhistorys))


@userstudyhistory.route("/user/<string:user>", methods=["POST"])
@jwt_required
def userstudyhistory_create(user):

    user_study_history_fields = userStudyHistorySchema.load(request.json)
    user_id = get_jwt_identity()

    user_object = User.query.get(user_id)

    if not user_object:
        return abort(404, description="User does not exist")



    # user_id = get_jwt_identity()
    user_study_history_object = UserStudyHistory()

    user_study_history_object.username = user_object.username
    user_study_history_object.qualification_title = user_study_history_fields["qualification_title"]
    user_study_history_object.institution = user_study_history_fields["institution"]
    user_study_history_object.city = user_study_history_fields["city"]
    user_study_history_object.country = user_study_history_fields["country"]
    user_study_history_object.date_start = user_study_history_fields["date_start"]
    user_study_history_object.date_end = user_study_history_fields["date_end"]
    user_study_history_object.last_updated = user_study_history_fields["last_updated"]

    db.session.add(user_study_history_object)
    
    db.session.commit()

    return jsonify(userStudyHistorySchema.dump(user_study_history_object))


@userstudyhistory.route("/<int:id>", methods=["GET"])
def userstudyhistory_get(id):
    #Return a single work history
    studyhistory = UserStudyHistory.query.get(id)
    return jsonify(userStudyHistorySchema.dump(studyhistory))

@userstudyhistory.route("/user/<int:id>", methods=["PUT", "PATCH"])
@jwt_required
def userstudyhistory_update(id):

    jwt_username = get_jwt_identity()

    userStudyHistory_fields = userStudyHistorySchema.load(request.json, partial=True)

    jwt_user = User.query.get(jwt_username)

    if not jwt_user:
        return abort(401, description="Invalid user")

    userStudyHistoryquery = UserStudyHistory.query.filter_by(id=id, username=jwt_username)

    if userStudyHistoryquery.count() != 1:
        return abort(401, description="Unauthorised to update this profile")

    userStudyHistoryquery.update(userStudyHistory_fields)
    db.session.commit()

    return jsonify(userStudyHistorySchema.dump(userStudyHistoryquery[0]))



@userstudyhistory.route("/<int:id>", methods=["DELETE"])
@jwt_required
def userstudyhistory_delete(id):

    #Delete a study history

    jwt_username = get_jwt_identity()

    userStudyHistory = UserStudyHistory.query.filter_by(id=id).first()

    if userStudyHistory is None:
        return abort(401, description=f"There does not exist a studyhistory with id {id}")


    if (jwt_username != userStudyHistory.username):
        return abort(401, description=f"You are logged in as username: {jwt_username} but the study history id matches to {userStudyHistory.username} ")

    # Check the user that wants to delete the studyhistory
    userStudyHistory = UserStudyHistory.query.filter_by(id=id, username=jwt_username).first()

    if not userStudyHistory:
        return abort(401, description=f"Study history Id of {id} does not exist for this user.")

    db.session.delete(userStudyHistory)
    db.session.commit()

    return jsonify(userStudyHistorySchema.dump(userStudyHistory))
