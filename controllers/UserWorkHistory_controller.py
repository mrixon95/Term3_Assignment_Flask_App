
from schemas.UserWorkHistorySchema import userWorkHistorySchema
from schemas.UserWorkHistorySchema import userWorkHistorySchemas
from models.User import User
from models.UserWorkHistory import UserWorkHistoryTable

from main import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify, abort
from sqlalchemy.orm import joinedload
userworkhistory = Blueprint('userworkhistory', __name__, url_prefix="/userworkhistory")

@userworkhistory.route("/", methods=["GET"])
def userworkhistory_all():
    # Retrieve all workhistorys
    userworkhistorys = UserWorkHistory.query.all()
    return jsonify(userWorkHistorySchemas.dump(userworkhistorys))


@userworkhistory.route("/user/<string:user>", methods=["GET"])
def userworkhistory_user(user):
    # Retrieve a particular users workhistorys

    user_object = User.query.get(user)

    if not user_object:
        return abort(401, description="Invalid user")

    user_work_histories_unordered = UserWorkHistory.query.filter_by(username=user)

    if not user_work_histories:
        return abort(404, description="No work histories to return")

    user_work_histories = user_work_histories_unordered.order_by(UserWorkHistoryTable.date_start.desc()).all()
    return jsonify(userWorkHistorySchemas.dump(userworkhistorys))


@userworkhistory.route("/user/<string:user>", methods=["POST"])
@jwt_required
def userworkhistory_create(user):

    user_work_history_fields = userWorkHistorySchema.load(request.json)
    user_id = get_jwt_identity()

    user_object = User.query.get(user_id)

    if not user_object:
        return abort(404, description="User does not exist")



    # user_id = get_jwt_identity()
    user_work_history_object = UserWorkHistory()

    user_work_history_object.username = user_object.username
    user_work_history_object.job_title = user_work_history_fields["job_title"]
    user_work_history_object.company = user_work_history_fields["company"]
    user_work_history_object.city = user_work_history_fields["city"]
    user_work_history_object.country = user_work_history_fields["country"]
    user_work_history_object.date_start = user_work_history_fields["date_start"]
    user_work_history_object.date_end = user_work_history_fields["date_end"]
    user_work_history_object.last_updated = user_work_history_fields["last_updated"]

    db.session.add(user_work_history_object)
    
    db.session.commit()

    return jsonify(userWorkHistorySchema.dump(user_work_history_object))


@userworkhistory.route("/<int:id>", methods=["GET"])
def userworkhistory_get(id):
    #Return a single work history
    workhistory = UserWorkHistoryTable.query.get(id)
    return jsonify(userWorkHistorySchema.dump(workhistory))

@userworkhistory.route("/user/<int:id>", methods=["PUT", "PATCH"])
@jwt_required
def userworkhistory_update(id):

    jwt_username = get_jwt_identity()

    userWorkHistory_fields = userWorkHistorySchema.load(request.json, partial=True)

    jwt_user = User.query.get(jwt_username)

    if not jwt_user:
        return abort(401, description="Invalid user")

    userWorkHistoryquery = UserWorkHistoryTable.query.filter_by(id=id, username=jwt_username)

    if userWorkHistoryquery.count() != 1:
        return abort(401, description="Unauthorised to update this profile")

    userWorkHistoryquery.update(userWorkHistory_fields)
    db.session.commit()

    return jsonify(userWorkHistorySchema.dump(userWorkHistoryquery[0]))



@userworkhistory.route("/<int:id>", methods=["DELETE"])
@jwt_required
def userworkhistory_delete(id):

    #Delete a work history

    jwt_username = get_jwt_identity()

    userWorkHistory = UserWorkHistory.query.filter_by(id=id).first()

    if userWorkHistory is None:
        return abort(401, description=f"There does not exist a workhistory with id {id}")


    if (jwt_username != userWorkHistory.username):
        return abort(401, description=f"You are logged in as username: {jwt_username} but the work history id matches to {userWorkHistory.username} ")

    # Check the user that wants to delete the workhistory
    userWorkHistory = UserWorkHistoryTable.query.filter_by(id=id, username=jwt_username).first()

    if not userWorkHistory:
        return abort(401, description=f"Work history Id of {id} does not exist for this user.")

    db.session.delete(userWorkHistory)
    db.session.commit()

    return jsonify(userWorkHistorySchema.dump(userWorkHistory))


