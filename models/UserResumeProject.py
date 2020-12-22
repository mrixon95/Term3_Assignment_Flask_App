from main import db
from datetime import datetime

class UserResumeProject(db.Model):
    __tablename__ = "userresumeprojects"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # username = db.Column(db.String(), db.ForeignKey("users.username"), nullable=False)
    resume_path = db.Column(db.String(), nullable=False)
    github_account = db.Column(db.String(), nullable=False)
    last_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # books = db.relationship("Book", backref="user", lazy="dynamic")

    def __repr__(self):
        return f"<UserResumeProject {self.id}>"