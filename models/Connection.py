from main import db
from models.BookImage import BookImage
from datetime import datetime

class Connection(db.Model):
    __tablename__ = "connections"
    
    user_id_1 = db.Column(db.Integer, db.ForeignKey("users.username"), primary_key=True)
    user_id_2 = db.Column(db.Integer, db.ForeignKey("users.username"), primary_key=True)
    last_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f"<Connection {self.user_id_1} {self.user_id_2}>"