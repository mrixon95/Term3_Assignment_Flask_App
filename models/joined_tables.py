from main import db


messages = db.Table(
    'messages',
    db.Column(
        'user_id_from', db.Integer, db.ForeignKey(
            'users.username', ondelete='CASCADE'), primary_key=True),
    db.Column(
        'user_id_to', db.Integer, db.ForeignKey(
            'users.username', ondelete='CASCADE'), primary_key=True),
    db.Column(
        'read', db.Boolean()),
    db.Column(
        'liked', db.Boolean()),
    db.Column(
        'sent_time', db.DateTime()),
    db.Column(
        'status', db.String(10))
)


connections = db.Table(
    'connections',
    db.Column(
        'user_id_from', db.Integer, db.ForeignKey(
            'users.username', ondelete='CASCADE'), primary_key=True),
    db.Column(
        'user_id_to', db.Integer, db.ForeignKey(
            'users.username', ondelete='CASCADE'), primary_key=True),
    db.Column(
        'status', db.String(10)),
    db.Column(
        'last_updated', db.DateTime())
)

