from flask import current_app
from sqlalchemy import desc

from ..models import Message


class MessageService:
    def save(self, message: Message):
        current_app.db.session.add(message)
        current_app.db.session.commit()

    def get_last_messages_by_chatroom(self, chatroom_id):
        messages = (
            Message.query.filter_by(chatroom_id=chatroom_id)
            .order_by(desc(Message.created_at))
            .limit(50)
            .all()
        )
        return messages
