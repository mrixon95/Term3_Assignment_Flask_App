
from schemas.WorkHistorySchema import work_history_schema
from schemas.WorkHistorySchema import work_history_schemas
from models.User import User
from models.WorkHistory import WorkHistory

from main import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify, abort
from sqlalchemy.orm import joinedload
workhistory = Blueprint('workhistory', __name__, url_prefix="/workhistory")

@workhistory.route("/", methods=["GET"])
def workhistory_all():
    # Retrieve all workhistorys
    work_histories = WorkHistory.query.all()
    return jsonify(work_history_schemas.dump(work_histories))


@workhistory.route("/user/<string:inputted_username>", methods=["GET"])
def workhistory_user(inputted_username):
    # Retrieve a particular users workhistorys

    print(inputted_username)
    user_object = User.query.get(inputted_username)

    if not user_object:
        return abort(401, description="Invalid user")

    work_histories_unordered = WorkHistory.query.filter_by(username=inputted_username)

    if not work_histories_unordered:
        return abort(404, description="No work histories to return")

    work_histories_ordered = work_histories_unordered.order_by(WorkHistory.date_start.desc()).all()
    return jsonify(work_history_schemas.dump(work_histories_ordered))


@workhistory.route("/", methods=["POST"])
@jwt_required
def workhistory_create():

    work_history_inputted_fields = work_history_schema.load(request.json)
    username_of_jwt = get_jwt_identity()

    user_of_jwt = User.query.get(username_of_jwt)

    if not user_of_jwt:
        return abort(404, description="User does not exist")



    # user_id = get_jwt_identity()
    work_history_object_from_fields = WorkHistory()

    work_history_object_from_fields.username = username_of_jwt
    work_history_object_from_fields.job_title = work_history_inputted_fields["job_title"]
    work_history_object_from_fields.company = work_history_inputted_fields["company"]
    work_history_object_from_fields.city = work_history_inputted_fields["city"]
    work_history_object_from_fields.country = work_history_inputted_fields["country"]
    work_history_object_from_fields.date_start = work_history_inputted_fields["date_start"]
    work_history_object_from_fields.date_end = work_history_inputted_fields["date_end"]
    work_history_object_from_fields.last_updated = work_history_inputted_fields["last_updated"]

    db.session.add(work_history_object_from_fields)
    
    db.session.commit()

    return jsonify(work_history_schema.dump(work_history_object_from_fields))


@workhistory.route("/<int:id>", methods=["GET"])
def workhistory_get(id):
    #Return a single work history
    work_history_object = WorkHistory.query.get(id)
    return jsonify(work_history_schema.dump(work_history_object))

@workhistory.route("/<int:id>", methods=["PUT", "PATCH"])
@jwt_required
def workhistory_update(id):

    jwt_username = get_jwt_identity()

    work_history_fields = work_history_schema.load(request.json, partial=True)

    jwt_user = User.query.get(jwt_username)

    if not jwt_user:
        return abort(401, description="Invalid user")

    work_history_object = WorkHistory.query.filter_by(id=id, username=jwt_username)

    if work_history_object.count() != 1:
        return abort(401, description=f"Work history with id {id} and username {jwt_username} does not exist")

    work_history_object.update(work_history_fields)
    db.session.commit()

    return jsonify(work_history_schema.dump(work_history_object[0]))



@workhistory.route("/<int:id>", methods=["DELETE"])
@jwt_required
def workhistory_delete(id):

    #Delete a work history

    jwt_username = get_jwt_identity()

    work_history_object = WorkHistory.query.filter_by(id=id).first()

    if work_history_object is None:
        return abort(401, description=f"There does not exist a workhistory with id {id}")


    if (jwt_username != work_history_object.username):
        return abort(401, description=f"The work history id belongs to a different user than your jwt token")

    # Check the user that wants to delete the workhistory
    work_history_object = WorkHistory.query.filter_by(id=id, username=jwt_username).first()

    if not work_history_object:
        return abort(401, description=f"Work history Id of {id} does not exist for this user.")

    db.session.delete(work_history_object)

    json_object_to_return = jsonify(work_history_schema.dump(work_history_object))

    db.session.commit()

    return json_object_to_return


