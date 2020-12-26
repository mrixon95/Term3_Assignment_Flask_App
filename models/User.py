from main import db
from datetime import datetime
from models.UserStudyHistory import UserStudyHistory
from models.UserWorkHistory import UserWorkHistory
from models.UserCertification import UserCertification
from models.UserResumeProject import UserResumeProject
from models.UserMeeting import UserMeeting


class User(db.Model):
    __tablename__ = "users"

    username = db.Column(db.String(), primary_key=True)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    dob = db.Column(db.DateTime, nullable=False)
    email = db.Column(db.String(), nullable=False, unique=True)
    mobile = db.Column(db.String())
    city = db.Column(db.String(), nullable=False)
    country = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    userstudyhistorys = db.relationship("UserStudyHistory", backref="user", lazy="dynamic")
    userworkhistorys = db.relationship("UserWorkHistory", backref="user", lazy="dynamic")
    usercertifications = db.relationship("UserCertification", backref="user", lazy="dynamic")
    userresumeprojects = db.relationship("UserResumeProject", backref="user", lazy="dynamic")
    usermeetings = db.relationship("UserMeeting", backref="user", lazy="dynamic")
    # books = db.relationship("Book", backref="user", lazy="dynamic")

    def __repr__(self):
        return f"<User {self.email}>"