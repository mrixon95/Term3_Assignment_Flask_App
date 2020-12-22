from main import db
from datetime import datetime

class UserWorkHistory(db.Model):
    __tablename__ = "userworkhistorys"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(), db.ForeignKey("users.username"), nullable=False)
    job_title = db.Column(db.String(), nullable=False)
    company = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(), nullable=False)
    country = db.Column(db.String(), nullable=False)
    date_start = db.Column(db.DateTime, nullable=False)
    date_end = db.Column(db.DateTime)
    last_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # books = db.relationship("Book", backref="user", lazy="dynamic")

    def __repr__(self):
        return f"<UserWorkHistory {self.id}>"