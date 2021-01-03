from main import db, bcrypt
from datetime import datetime
from models.StudyHistory import StudyHistory
from models.WorkHistory import WorkHistory
from models.Certification import Certification
from models.ResumeProject import ResumeProject
from models.Meeting import Meeting
# from models.joined_tables import message
from models.Message import Message
from models.Connection import Connection
from models.Post import Post
from models.Likes_Table import Likes_Table
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
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
    studyhistorys = db.relationship("StudyHistory", backref="user", lazy="dynamic")
    workhistorys = db.relationship("WorkHistory", backref="user", lazy="dynamic")
    certifications = db.relationship("Certification", backref="user", lazy="dynamic")
    resumeprojects = db.relationship("ResumeProject", backref="user", lazy="dynamic")

    # usermeetings = db.relationship("UserMeeting", backref="user", lazy="dynamic")
    # messages = db.relationship("Message", backref="username_of_sender", lazy="dynamic")

    
    likes = db.relationship(
        "Likes_Table",
        foreign_keys="Likes_Table.username_of_liker",
        backref ="user"
    )


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


    
    def get_id(self):
        try:
            return str(self.username)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')
    
    
    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)







    def __repr__(self):
        return f"<User {self.email}>"