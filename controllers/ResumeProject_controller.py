from schemas.ResumeProjectSchema import resume_project_schema
from schemas.ResumeProjectSchema import resume_project_schemas
from models.User import User
from models.ResumeProject import ResumeProject

from main import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify, abort
from sqlalchemy.orm import joinedload
resumeproject = Blueprint('resumeproject', __name__, url_prefix="/resumeproject")

@resumeproject.route("/", methods=["GET"])
def resumeproject_all():
    # Retrieve all workhistorys
    resume_project_objects = ResumeProject.query.all()
    return jsonify(resume_project_schemas.dump(resume_project_objects))


@resumeproject.route("/user/<string:inputted_username>", methods=["GET"])
def resumeproject_user(inputted_username):
    # Retrieve a particular users workhistorys

    user_object = User.query.get(inputted_username)

    if not user_object:
        return abort(401, description="Invalid user")

    resume_project_unordered = ResumeProject.query.filter_by(username=inputted_username)

    if not resume_project_unordered:
        return abort(404, description="No work histories to return")

    resume_project_ordered = resume_project_unordered.order_by(ResumeProject.date_start.desc()).all()
    return jsonify(resume_project_schemas.dump(resume_project_ordered))


@resumeproject.route("/", methods=["POST"])
@jwt_required
def resumeproject_create():

    resume_project_inputted_fields = resume_project_schema.load(request.json)
    username_of_jwt = get_jwt_identity()

    user_of_jwt = User.query.get(username_of_jwt)

    if not user_of_jwt:
        return abort(404, description="User does not exist")



    # user_id = get_jwt_identity()
    resume_project_object_from_fields = ResumeProject()

    resume_project_object_from_fields.username = username_of_jwt
    resume_project_object_from_fields.job_title = resume_project_inputted_fields["job_title"]
    resume_project_object_from_fields.company = resume_project_inputted_fields["company"]
    resume_project_object_from_fields.city = resume_project_inputted_fields["city"]
    resume_project_object_from_fields.country = resume_project_inputted_fields["country"]
    resume_project_object_from_fields.date_start = resume_project_inputted_fields["date_start"]
    resume_project_object_from_fields.date_end = resume_project_inputted_fields["date_end"]
    resume_project_object_from_fields.last_updated = resume_project_inputted_fields["last_updated"]

    db.session.add(resume_project_object_from_fields)
    
    db.session.commit()

    return jsonify(resume_project_schema.dump(resume_project_object_from_fields))


@resumeproject.route("/<int:id>", methods=["GET"])
def resumeproject_get(id):
    #Return a single work history
    resume_project_object = ResumeProject.query.get(id)
    return jsonify(resume_project_schema.dump(resume_project_object))

@resumeproject.route("/<int:id>", methods=["PUT", "PATCH"])
@jwt_required
def resumeproject_update(id):

    jwt_username = get_jwt_identity()

    resume_project_fields = resume_project_schema.load(request.json, partial=True)

    jwt_user = User.query.get(jwt_username)

    if not jwt_user:
        return abort(401, description="Invalid user")

    resume_project_object = ResumeProject.query.filter_by(id=id, username=jwt_username)

    if resume_project_object.count() != 1:
        return abort(401, description="Unauthorised to update this profile")

    resume_project_object.update(resume_project_fields)
    db.session.commit()

    return jsonify(resume_project_schema.dump(resume_project_object[0]))



@resumeproject.route("/<int:id>", methods=["DELETE"])
@jwt_required
def resumeproject_delete(id):

    #Delete a work history

    jwt_username = get_jwt_identity()

    resume_project_object = ResumeProject.query.filter_by(id=id).first()

    if resume_project_object is None:
        return abort(401, description=f"There does not exist a workhistory with id {id}")


    if (jwt_username != resume_project_object.username):
        return abort(401, description=f"You are logged in as username: {jwt_username} but the work history id matches to {resume_project_object.username} ")

    # Check the user that wants to delete the workhistory
    resume_project_object = ResumeProject.query.filter_by(id=id, username=jwt_username).first()

    if not resume_project_object:
        return abort(401, description=f"Work history Id of {id} does not exist for this user.")

    db.session.delete(resume_project_object)

    json_object_to_return = jsonify(resume_project_schema.dump(resume_project_object))

    db.session.commit()

    return json_object_to_return


