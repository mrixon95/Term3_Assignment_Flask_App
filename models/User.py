from main import db
from datetime import datetime
from models.UserStudyHistory import UserStudyHistory
from models.UserWorkHistory import UserWorkHistory
from models.UserCertification import UserCertification
from models.UserResumeProject import UserResumeProject
from models.UserMeeting import UserMeeting
# from models.joined_tables import message
from models.Message import Message
from models.Connection import Connection

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
    # usermeetings = db.relationship("UserMeeting", backref="user", lazy="dynamic")
    # messages = db.relationship("Message", backref="username_of_sender", lazy="dynamic")

    messages1 = db.relationship(
        "Message",
        foreign_keys="Message.username_of_sender",
        backref ="sender"
    )

    messages2 = db.relationship(
        "Message",
        foreign_keys="Message.username_of_receiver",
        backref ="receiver"
    )

    connection1 = db.relationship(
        "Connection",
        foreign_keys="Connection.username_of_requester",
        backref ="requester"
    )

    connection2 = db.relationship(
        "Connection",
        foreign_keys="Connection.username_of_confirmer",
        backref ="confirmer"
    )

    # books = db.relationship("Book", backref="user", lazy="dynamic")

    def __repr__(self):
        return f"<User {self.email}>"