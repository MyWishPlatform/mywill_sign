from app import db
from sqlalchemy.dialects.postgresql import JSON


class Account(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True)
    priv = db.Column(db.String())
    pub = db.Column(db.String())
    addr = db.Column(db.String())
    used = db.Column(db.Boolean())
