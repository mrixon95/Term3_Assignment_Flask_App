from schemas.CertificationSchema import certification_schema
from schemas.CertificationSchema import certification_schemas
from models.User import User
from models.Certification import Certification

from main import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify, abort
from sqlalchemy.orm import joinedload
from schemas.CertificationSchema import certification_schema
from schemas.CertificationSchema import certification_schemas


certification = Blueprint('certification', __name__, url_prefix="/certification")

@certification.route("/", methods=["GET"])
def certificationhistory_all():
    # Retrieve all workhistorys
    certifications = Certification.query.all()
    return jsonify(certification_schemas.dump(certifications))


@certification.route("/<string:inputted_username>", methods=["GET"])
def certificationhistory_user(inputted_username):
    # Retrieve a particular users workhistorys

    user_object = User.query.get(inputted_username)

    if not user_object:
        return abort(401, description="Invalid user")

    user_certifications_unordered = Certification.query.filter_by(username=inputted_username)

    if not user_certifications_unordered:
        return abort(404, description="No work histories to return")

    user_certifications_ordered = user_certifications_unordered.order_by(Certification.date_start.desc()).all()
    return jsonify(certification_schemas.dump(user_certifications_ordered))


@certification.route("/", methods=["POST"])
@jwt_required
def certificationhistory_create():

    certification_inputted_fields = certification_schema.load(request.json)
    username_of_jwt = get_jwt_identity()

    user_of_jwt = User.query.get(username_of_jwt)

    if not user_of_jwt:
        return abort(404, description="User does not exist")



    # user_id = get_jwt_identity()
    certification_object_from_fields = Certification()

    certification_object_from_fields.username = username_of_jwt
    certification_object_from_fields.cert_name = certification_inputted_fields["cert_name"]
    certification_object_from_fields.description = certification_inputted_fields["description"]
    certification_object_from_fields.issuer = certification_inputted_fields["issuer"]
    certification_object_from_fields.date_obtained = certification_inputted_fields["date_obtained"]
    certification_object_from_fields.last_updated = certification_inputted_fields["last_updated"]

    db.session.add(certification_object_from_fields)
    
    db.session.commit()

    return jsonify(certification_schema.dump(certification_object_from_fields))


@certification.route("/<int:id>", methods=["GET"])
def certificationhistory_get(id):
    #Return a single work history
    certification_object = Certification.query.get(id)
    return jsonify(certification_schema.dump(certification_object))

@certification.route("/<int:id>", methods=["PUT", "PATCH"])
@jwt_required
def certificationhistory_update(id):

    jwt_username = get_jwt_identity()

    certification_fields = certification_schema.load(request.json, partial=True)

    jwt_user = User.query.get(jwt_username)

    if not jwt_user:
        return abort(401, description="Invalid user")

    certification_object = Certification.query.filter_by(id=id, username=jwt_username)

    if certification_object.count() != 1:
        return abort(401, description="Unauthorised to update this profile")

    certification_object.update(certification_fields)
    db.session.commit()

    return jsonify(certification_schema.dump(certification_object[0]))



@certification.route("/<int:id>", methods=["DELETE"])
@jwt_required
def certificationhistory_delete(id):

    #Delete a work history

    jwt_username = get_jwt_identity()

    certification_object = Certification.query.filter_by(id=id).first()

    if certification_object is None:
        return abort(401, description=f"There does not exist a certification with id {id}")


    if (jwt_username != certification_object.username):
        return abort(401, description=f"You are logged in as username: {jwt_username} but the certification id matches to {certification_object.username} ")

    # Check the user that wants to delete the workhistory

    certification_object = Certification.query.filter_by(id=id, username=jwt_username).first()

    if not certification_object:
        return abort(401, description=f"usercertification Id of {id} does not exist for this user.")

    db.session.delete(certification_object)

    json_object_to_return = jsonify(certification_schema.dump(certification_object))

    db.session.commit()

    return json_object_to_return


