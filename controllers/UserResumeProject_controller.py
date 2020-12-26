from schemas.UserResumeProjectSchema import user_resume_project_schema
from schemas.UserResumeProjectSchema import user_resume_project_schemas
from models.User import User
from models.UserResumeProject import UserResumeProject

from main import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify, abort
from sqlalchemy.orm import joinedload
userresumeproject = Blueprint('userresumeproject', __name__, url_prefix="/userresumeproject")

@userresumeproject.route("/", methods=["GET"])
def userresumeproject_all():
    # Retrieve all workhistorys
    user_resume_project_objects = UserResumeProject.query.all()
    return jsonify(user_resume_project_schemas.dump(user_resume_project_objects))


@userresumeproject.route("/user/<string:inputted_username>", methods=["GET"])
def userresumeproject_user(inputted_username):
    # Retrieve a particular users workhistorys

    user_object = User.query.get(inputted_username)

    if not user_object:
        return abort(401, description="Invalid user")

    user_resume_project_unordered = UserResumeProject.query.filter_by(username=inputted_username)

    if not user_resume_project_unordered:
        return abort(404, description="No work histories to return")

    user_resume_project_ordered = user_resume_project_unordered.order_by(UserResumeProject.date_start.desc()).all()
    return jsonify(user_resume_project_schemas.dump(user_resume_project_ordered))


@userresumeproject.route("/", methods=["POST"])
@jwt_required
def userresumeproject_create():

    user_resume_project_inputted_fields = user_resume_project_schema.load(request.json)
    username_of_jwt = get_jwt_identity()

    user_of_jwt = User.query.get(username_of_jwt)

    if not user_of_jwt:
        return abort(404, description="User does not exist")



    # user_id = get_jwt_identity()
    user_resume_project_object_from_fields = UserResumeProject()

    user_resume_project_object_from_fields.username = username_of_jwt
    user_resume_project_object_from_fields.job_title = user_resume_project_inputted_fields["job_title"]
    user_resume_project_object_from_fields.company = user_resume_project_inputted_fields["company"]
    user_resume_project_object_from_fields.city = user_resume_project_inputted_fields["city"]
    user_resume_project_object_from_fields.country = user_resume_project_inputted_fields["country"]
    user_resume_project_object_from_fields.date_start = user_resume_project_inputted_fields["date_start"]
    user_resume_project_object_from_fields.date_end = user_resume_project_inputted_fields["date_end"]
    user_resume_project_object_from_fields.last_updated = user_resume_project_inputted_fields["last_updated"]

    db.session.add(user_resume_project_object_from_fields)
    
    db.session.commit()

    return jsonify(user_resume_project_schema.dump(user_resume_project_object_from_fields))


@userresumeproject.route("/<int:id>", methods=["GET"])
def userresumeproject_get(id):
    #Return a single work history
    user_resume_project_object = UserResumeProject.query.get(id)
    return jsonify(user_resume_project_schema.dump(user_resume_project_object))

@userresumeproject.route("/<int:id>", methods=["PUT", "PATCH"])
@jwt_required
def userresumeproject_update(id):

    jwt_username = get_jwt_identity()

    user_resume_project_fields = user_resume_project_schema.load(request.json, partial=True)

    jwt_user = User.query.get(jwt_username)

    if not jwt_user:
        return abort(401, description="Invalid user")

    user_resume_project_object = UserResumeProject.query.filter_by(id=id, username=jwt_username)

    if user_resume_project_object.count() != 1:
        return abort(401, description="Unauthorised to update this profile")

    user_resume_project_object.update(user_resume_project_fields)
    db.session.commit()

    return jsonify(user_resume_project_schema.dump(user_resume_project_object[0]))



@userresumeproject.route("/<int:id>", methods=["DELETE"])
@jwt_required
def userresumeproject_delete(id):

    #Delete a work history

    jwt_username = get_jwt_identity()

    user_resume_project_object = UserResumeProject.query.filter_by(id=id).first()

    if user_resume_project_object is None:
        return abort(401, description=f"There does not exist a workhistory with id {id}")


    if (jwt_username != user_resume_project_object.username):
        return abort(401, description=f"You are logged in as username: {jwt_username} but the work history id matches to {user_work_history_object.username} ")

    # Check the user that wants to delete the workhistory
    user_resume_project_object = UserResumeProject.query.filter_by(id=id, username=jwt_username).first()

    if not user_resume_project_object:
        return abort(401, description=f"Work history Id of {id} does not exist for this user.")

    db.session.delete(user_resume_project_object)

    json_object_to_return = jsonify(user_resume_project_schema.dump(user_resume_project_object))

    db.session.commit()

    return json_object_to_return


