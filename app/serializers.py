from flask_marshmallow import Marshmallow
from marshmallow import ValidationError, validates
from marshmallow_sqlalchemy import auto_field, fields

from .models import Chatroom, Message, User

ma = Marshmallow()


def configure(app):
    ma.init_app(app)


class ChatroomSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Chatroom
        load_instance = True
        sqla_session = True

    author_id = auto_field(load_only=True)
    author = fields.Nested(lambda: UserSchema(only=("id", "username")), dump_only=True)

    @validates("author_id")
    def validate_author_id(self, author_id):
        user = User.query.get(author_id)
        if user is None:
            raise ValidationError("User does not exist")


class MessageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Message
        load_instance = True
        sqla_session = True

    author_id = auto_field(load_only=True)
    author = fields.Nested(lambda: UserSchema(only=("id", "username")), dump_only=True)

    @validates("author_id")
    def validate_author_id(self, author_id):
        user = User.query.get(author_id)
        if user is None:
            raise ValidationError("User does not exist")

    chatroom_id = auto_field(load_only=True)

    @validates("chatroom_id")
    def validate_chatroom_id(self, chatroom_id):
        user = Chatroom.query.get(chatroom_id)
        if user is None:
            raise ValidationError("Chatroom does not exist")


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        sqla_session = True

    password = auto_field(load_only=True)
