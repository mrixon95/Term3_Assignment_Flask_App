from main import db
from datetime import datetime

class ITNews(db.Model):
    __tablename__ = "itnews"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    article_link = db.Column(db.String(), nullable=False)
    photo_link = db.Column(db.String(), nullable=False)
    published_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # books = db.relationship("Book", backref="user", lazy="dynamic")

    def __repr__(self):
        return f"<ITNews {self.id}>"