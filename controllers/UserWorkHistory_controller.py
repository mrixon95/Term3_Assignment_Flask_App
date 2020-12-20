
from schemas.UserWorkHistorySchema import user_work_history_schema
from schemas.UserWorkHistorySchema import user_work_history_schemas
from models.User import User
from models.UserWorkHistory import UserWorkHistory

from main import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify, abort
from sqlalchemy.orm import joinedload
userworkhistory = Blueprint('userworkhistory', __name__, url_prefix="/userworkhistory")

@userworkhistory.route("/", methods=["GET"])
def userworkhistory_all():
    # Retrieve all workhistorys
    user_work_histories = UserWorkHistory.query.all()
    return jsonify(user_work_history_schemas.dump(user_work_histories))


@userworkhistory.route("/user/<string:inputted_username>", methods=["GET"])
def userworkhistory_user(inputted_username):
    # Retrieve a particular users workhistorys

    user_object = User.query.get(inputted_username)

    if not user_object:
        return abort(401, description="Invalid user")

    user_work_histories_unordered = UserWorkHistory.query.filter_by(username=inputted_username)

    if not user_work_histories_unordered:
        return abort(404, description="No work histories to return")

    user_work_histories_ordered = user_work_histories_unordered.order_by(UserWorkHistory.date_start.desc()).all()
    return jsonify(user_work_history_schemas.dump(user_work_histories_ordered))


@userworkhistory.route("/user/<string:inputted_username>", methods=["POST"])
@jwt_required
def userworkhistory_create(inputted_username):

    user_work_history_inputted_fields = user_work_history_schemas.load(request.json)
    username_of_jwt = get_jwt_identity()

    user_of_jwt = User.query.get(username_of_jwt)

    if not user_of_jwt:
        return abort(404, description="User does not exist")



    # user_id = get_jwt_identity()
    user_work_history_object_from_fields = UserWorkHistory()

    user_work_history_object_from_fields.username = username_of_jwt
    user_work_history_object_from_fields.job_title = user_work_history_inputted_fields["job_title"]
    user_work_history_object_from_fields.company = user_work_history_inputted_fields["company"]
    user_work_history_object_from_fields.city = user_work_history_inputted_fields["city"]
    user_work_history_object_from_fields.country = user_work_history_inputted_fields["country"]
    user_work_history_object_from_fields.date_start = user_work_history_inputted_fields["date_start"]
    user_work_history_object_from_fields.date_end = user_work_history_inputted_fields["date_end"]
    user_work_history_object_from_fields.last_updated = user_work_history_inputted_fields["last_updated"]

    db.session.add(user_work_history_object_from_fields)
    
    db.session.commit()

    return jsonify(user_work_history_schema.dump(user_work_history_object_from_fields))


@userworkhistory.route("/<int:id>", methods=["GET"])
def userworkhistory_get(id):
    #Return a single work history
    user_work_history_object = UserWorkHistory.query.get(id)
    return jsonify(user_work_history_schema.dump(user_work_history_object))

@userworkhistory.route("/user/<int:id>", methods=["PUT", "PATCH"])
@jwt_required
def userworkhistory_update(id):

    jwt_username = get_jwt_identity()

    user_work_history_fields = user_work_history_schema.load(request.json, partial=True)

    jwt_user = User.query.get(jwt_username)

    if not jwt_user:
        return abort(401, description="Invalid user")

    user_work_history_object = UserWorkHistory.query.filter_by(id=id, username=jwt_username)

    if user_work_history_object.count() != 1:
        return abort(401, description="Unauthorised to update this profile")

    user_work_history_object.update(user_work_history_fields)
    db.session.commit()

    return jsonify(user_work_history_schema.dump(user_work_history_object[0]))



@userworkhistory.route("/<int:id>", methods=["DELETE"])
@jwt_required
def userworkhistory_delete(id):

    #Delete a work history

    jwt_username = get_jwt_identity()

    user_work_history_object = UserWorkHistory.query.filter_by(id=id).first()

    if user_work_history_object is None:
        return abort(401, description=f"There does not exist a workhistory with id {id}")


    if (jwt_username != user_work_history_object.username):
        return abort(401, description=f"You are logged in as username: {jwt_username} but the work history id matches to {user_work_history_object.username} ")

    # Check the user that wants to delete the workhistory
    user_work_history_object = UserWorkHistory.query.filter_by(id=id, username=jwt_username).first()

    if not user_work_history_object:
        return abort(401, description=f"Work history Id of {id} does not exist for this user.")

    db.session.delete(user_work_history_object)
    db.session.commit()

    return jsonify(user_work_history_schema.dump(user_work_history_object))


