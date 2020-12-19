from main import db
from datetime import datetime

class JobSalary(db.Model):
    __tablename__ = "jobsalaries"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(), nullable=False)
    lower_quartile = db.Column(db.Integer(), nullable=False)
    median_salary = db.Column(db.Integer(), nullable=False)
    upper_quartile = db.Column(db.Integer(), nullable=False)
    average_years_experience = db.Column(db.DateTime, nullable=False)
    last_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # books = db.relationship("Book", backref="user", lazy="dynamic")

    def __repr__(self):
        return f"<JobSalary {self.id}>"