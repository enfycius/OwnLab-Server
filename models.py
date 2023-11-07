from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = "user"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    pwd = db.Column(db.String(300), nullable=False, unique=True)
    tel = db.Column(db.String(11), nullable=False, unique=True)

    def __repr__(self):
        return '<User %r>' % self.username
    
class File(db.Model):
    __tablename__ = "file"
    
    id = db.Column(db.Integer, primary_key=True)
    dir = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<Root %r>' % self.root