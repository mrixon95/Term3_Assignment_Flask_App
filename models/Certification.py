from main import db
from datetime import datetime

class Certification(db.Model):
    __tablename__ = "certifications"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(), db.ForeignKey("users.username"), nullable=False)
    cert_name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    issuer = db.Column(db.String(), nullable=False)
    date_obtained = db.Column(db.DateTime, nullable=False)
    last_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Certification {self.id}>"