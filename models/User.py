from main import db
from datetime import datetime
from models.UserStudyHistory import UserStudyHistory
from models.UserWorkHistory import UserWorkHistory


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
    userstudyhistorys = db.relationship("UserStudyHistory", backref="users", lazy="dynamic")
    userworkhistorys = db.relationship("UserWorkHistory", backref="users", lazy="dynamic")
    # books = db.relationship("Book", backref="user", lazy="dynamic")

    def __repr__(self):
        return f"<User {self.email}>"