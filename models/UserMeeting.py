from main import db
from datetime import datetime

class UserMeeting(db.Model):
    __tablename__ = "usermeetings"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(), db.ForeignKey("users.username"), nullable=False)
    time_start = db.Column(db.DateTime, nullable=False)
    time_end = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(), nullable=False)
    subject = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    last_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<UserMeeting {self.id}>"