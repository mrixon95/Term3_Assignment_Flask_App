from main import db
from datetime import datetime
from sqlalchemy.orm import relationship
# from models.joined_tables import messages


class Message(db.Model):
    __tablename__ = "Message"
    __table_args__ = (
        db.CheckConstraint('username_of_sender != username_of_receiver'),
    )
    id = db.Column(db.Integer, primary_key=True)
    username_of_sender = db.Column(
        db.String(), db.ForeignKey('users.username'))
    username_of_receiver = db.Column(
        db.String(), db.ForeignKey('users.username'))
    content = db.Column(db.String(), nullable=False)
    read = db.Column(db.Boolean, default=False)
    liked = db.Column(db.Boolean, default=False)
    sent_time = db.Column(db.DateTime, default=datetime.utcnow)

    # username_from = db.relationship("User", foreign_keys=[username_from_id])
    # username_to = db.relationship("User", foreign_keys=[username_to_id])

    # usernames= db.relationship("User", foreign_keys=[username_from_id, username_to_id])