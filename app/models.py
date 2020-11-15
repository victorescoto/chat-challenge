from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import pbkdf2_sha256

from .exceptions import InvalidPasswordException

db = SQLAlchemy()


def configure(app):
    db.init_app(app)
    app.db = db


class Chatroom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    author = db.relationship("User", backref=db.backref("chatrooms", cascade="all, delete-orphan"))


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chatroom_id = db.Column(db.Integer, db.ForeignKey("chatroom.id"), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    content = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    chatroom = db.relationship("Chatroom", backref=db.backref("messages", cascade="all, delete-orphan"))
    author = db.relationship("User", backref=db.backref("messages", cascade="all, delete-orphan"))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def hash_password(self):
        self.password = pbkdf2_sha256.hash(self.password)

    def verify_password(self, password):
        valid = pbkdf2_sha256.verify(password, self.password)
        if not valid:
            raise InvalidPasswordException()
