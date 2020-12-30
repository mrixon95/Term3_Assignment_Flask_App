
from schemas.JobSalarySchema import job_salary_schema
from schemas.JobSalarySchema import job_salary_schemas
from models.User import User
from models.JobSalary import JobSalary

from main import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify, abort
from sqlalchemy.orm import joinedload
jobsalary = Blueprint('jobsalary', __name__, url_prefix="/jobsalary")

@jobsalary.route("/", methods=["GET"])
def jobsalary_all():
    # Retrieve all workhistorys
    job_salaries = JobSalary.query.all()
    return jsonify(job_salary_schemas.dump(job_salaries))


@jobsalary.route("/", methods=["POST"])
def jobsalary_create():

    job_salary_object = job_salary_schemas.load(request.json)

    db.session.add(job_salary_object)
    
    db.session.commit()

    return jsonify(job_salary_schema.dump(job_salary_object))


@jobsalary.route("/<int:id>", methods=["GET"])
def jobsalary_get(id):
    #Return a single work history
    job_salary_object = JobSalary.query.get(id)
    return jsonify(job_salary_schema.dump(job_salary_object))


@jobsalary.route("/<int:id>", methods=["PUT", "PATCH"])
def jobsalary_update(id):

    job_salary_fields = job_salary_schema.load(request.json, partial=True)

    job_salary_object = JobSalary.query.filter_by(id=id)

    if job_salary_object.count() != 1:
        return abort(401, description=f"Job salary with id {id} does not exist")

    job_salary_object.update(job_salary_fields)
    db.session.commit()

    return jsonify(job_salary_schema.dump(job_salary_object[0]))



@jobsalary.route("/<int:id>", methods=["DELETE"])
def jobsalary_delete(id):

    #Delete a work history

    job_salary_object = JobSalary.query.filter_by(id=id).first()

    if job_salary_object is None:
        return abort(401, description=f"There does not exist a job salary with id {id}")

    # Check the user that wants to delete the workhistory
    job_salary_object = JobSalary.query.filter_by(id=id).first()

    if not job_salary_object:
        return abort(401, description=f"job salary of {id} does not exist for this user.")

    json_object_to_return = jsonify(job_salary_schema.dump(job_salary_object))

    db.session.delete(job_salary_object)

    db.session.commit()

    return json_object_to_return


