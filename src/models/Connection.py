from main import db
from datetime import datetime
from marshmallow import validate

class Connection(db.Model):
    __tablename__ = "connections"
    # id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    __table_args__ = (
        db.CheckConstraint('username_of_requester != username_of_confirmer'),
    )
    username_of_requester = db.Column(db.String(), db.ForeignKey("users.username"), primary_key=True)
    username_of_confirmer = db.Column(db.String(), db.ForeignKey("users.username"), primary_key=True)
    user_1_approved = db.Column(db.Boolean, default=True)
    user_2_approved = db.Column(db.Boolean, default=False)
    last_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(), default='pending')

    def __repr__(self):
        return f"<Connection {self.username_of_requester} {self.username_of_confirmer}>"