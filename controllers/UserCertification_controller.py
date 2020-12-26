from schemas.UserCertificationSchema import user_certification_schema
from schemas.UserCertificationSchema import user_certification_schemas
from models.User import User
from models.UserCertification import UserCertification

from main import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify, abort
from sqlalchemy.orm import joinedload
from schemas.UserCertificationSchema import user_certification_schema
from schemas.UserCertificationSchema import user_certification_schemas


usercertification = Blueprint('usercertification', __name__, url_prefix="/usercertification")

@usercertification.route("/", methods=["GET"])
def usercertificationhistory_all():
    # Retrieve all workhistorys
    user_certifications = UserCertification.query.all()
    return jsonify(user_certification_schemas.dump(user_certifications))


@usercertification.route("/<string:inputted_username>", methods=["GET"])
def usercertificationhistory_user(inputted_username):
    # Retrieve a particular users workhistorys

    user_object = User.query.get(inputted_username)

    if not user_object:
        return abort(401, description="Invalid user")

    user_certifications_unordered = UserCertification.query.filter_by(username=inputted_username)

    if not user_certifications_unordered:
        return abort(404, description="No work histories to return")

    user_certifications_ordered = user_certifications_unordered.order_by(UserCertification.date_start.desc()).all()
    return jsonify(user_certification_schemas.dump(user_certifications_ordered))


@usercertification.route("/", methods=["POST"])
@jwt_required
def usercertificationhistory_create():

    user_certification_inputted_fields = user_certification_schema.load(request.json)
    username_of_jwt = get_jwt_identity()

    user_of_jwt = User.query.get(username_of_jwt)

    if not user_of_jwt:
        return abort(404, description="User does not exist")



    # user_id = get_jwt_identity()
    user_certification_object_from_fields = UserCertification()

    user_certification_object_from_fields.username = username_of_jwt
    user_certification_object_from_fields.cert_name = user_certification_inputted_fields["cert_name"]
    user_certification_object_from_fields.description = user_certification_inputted_fields["description"]
    user_certification_object_from_fields.issuer = user_certification_inputted_fields["issuer"]
    user_certification_object_from_fields.date_obtained = user_certification_inputted_fields["date_obtained"]
    user_certification_object_from_fields.last_updated = user_certification_inputted_fields["last_updated"]

    db.session.add(user_certification_object_from_fields)
    
    db.session.commit()

    return jsonify(user_certification_schema.dump(user_certification_object_from_fields))


@usercertification.route("/<int:id>", methods=["GET"])
def usercertificationhistory_get(id):
    #Return a single work history
    user_certification_object = UserCertification.query.get(id)
    return jsonify(user_certification_schema.dump(user_certification_object))

@usercertification.route("/<int:id>", methods=["PUT", "PATCH"])
@jwt_required
def usercertificationhistory_update(id):

    jwt_username = get_jwt_identity()

    user_certification_fields = user_certification_schema.load(request.json, partial=True)

    jwt_user = User.query.get(jwt_username)

    if not jwt_user:
        return abort(401, description="Invalid user")

    user_certification_object = UserCertification.query.filter_by(id=id, username=jwt_username)

    if user_certification_object.count() != 1:
        return abort(401, description="Unauthorised to update this profile")

    user_certification_object.update(user_certification_fields)
    db.session.commit()

    return jsonify(user_certification_schema.dump(user_certification_object[0]))



@usercertification.route("/<int:id>", methods=["DELETE"])
@jwt_required
def usercertificationhistory_delete(id):

    #Delete a work history

    jwt_username = get_jwt_identity()

    user_certification_object = UserCertification.query.filter_by(id=id).first()

    if user_certification_object is None:
        return abort(401, description=f"There does not exist a usercertification with id {id}")


    if (jwt_username != user_certification_object.username):
        return abort(401, description=f"You are logged in as username: {jwt_username} but the usercertification id matches to {user_certification_object.username} ")

    # Check the user that wants to delete the workhistory

    user_certification_object = UserCertification.query.filter_by(id=id, username=jwt_username).first()

    if not user_certification_object:
        return abort(401, description=f"usercertification Id of {id} does not exist for this user.")

    db.session.delete(user_certification_object)

    json_object_to_return = jsonify(user_certification_schema.dump(user_certification_object))

    db.session.commit()

    return json_object_to_return


