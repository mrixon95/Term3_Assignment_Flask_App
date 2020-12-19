from main import db
from datetime import datetime

class Meeting(db.Model):
    __tablename__ = "meetings"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(), db.ForeignKey("users.username"), nullable=False)
    time_start = db.Column(db.DateTime) 
    time_end = db.Column(db.DateTime)
    location = db.Column(db.String(), nullable=False)
    subject = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    last_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # books = db.relationship("Book", backref="user", lazy="dynamic")

    def __repr__(self):
        return f"<Meeting {self.id}>"