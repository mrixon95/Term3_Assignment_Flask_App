from main import db
from datetime import datetime
from models.Likes_Table import Likes_Table

class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(), db.ForeignKey("users.username"), nullable=False)
    content = db.Column(db.String(), nullable=False)
    likes = db.Column(db.Integer(), nullable=False, default=0)
    last_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    posts = db.relationship(
        "Likes_Table",
        foreign_keys="Likes_Table.post_id",
        backref ="post"
    )


    def __repr__(self):
        return f"<Post {self.id}>"