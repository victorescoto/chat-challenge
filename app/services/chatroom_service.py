from flask import current_app

from ..models import Chatroom


class ChatroomService:
    def list(self):
        chatrooms = Chatroom.query.all()
        return chatrooms

    def get(self, id: int):
        chatroom = Chatroom.query.get(id)
        return chatroom

    def save(self, chatroom: Chatroom):
        current_app.db.session.add(chatroom)
        current_app.db.session.commit()

    def delete(self, chatroom: Chatroom):
        current_app.db.session.delete(chatroom)
        current_app.db.session.commit()
