from main import db
from datetime import datetime
from marshmallow import validate

class Likes_Table(db.Model):
    __tablename__ = "likes"
    # id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    post_id = db.Column(db.Integer(), db.ForeignKey("posts.id"), primary_key=True)
    username_of_liker = db.Column(db.String(), db.ForeignKey("users.username"), primary_key=True)

    def __repr__(self):
        return f"<Connection {self.post_id} {self.username_of_like}>"