import json
import re
from threading import Thread

from flask import current_app, session
from flask_login import current_user
from flask_socketio import emit, join_room, leave_room

from .. import socketio
from ..commands import StockCommand
from ..models import Message
from ..services import MessageService, RabbitMQService


@socketio.on("joined")
def joined(json):
    room = int(json["chatroom"])
    session["chatroom_id"] = room
    join_room(room)
    emit(
        "status",
        {"msg": current_user.username + " has entered the room.", "type": "join"},
        room=room,
    )


@socketio.on("text")
def text(json):
    room = session.get("chatroom_id")
    message = json["content"]

    if re.search(r"/", message):
        handle_command(message, room)
        return

    message = Message(content=message, chatroom_id=room, author_id=current_user.id)

    MessageService().save(message)

    emit(
        "message",
        {
            "content": message.content,
            "createdAt": str(message.created_at),
            "author": {"id": message.author.id, "username": message.author.username},
        },
        room=room,
    )


def handle_command(command, room):
    if re.search(r"/stock=", command):
        StockCommand().send_to_queue(command, room)
        emit("status", {"msg": "stock command accepted.", "type": "command"}, room=room)
        return

    emit("status", {"msg": f"{command} command nof found.", "type": "error"}, room=room)


def consumer(app):
    with app.app_context():
        def callback(ch, method, properties, body):
            params = json.loads(body.decode("utf-8"))
            if "message" in params:
                emit(
                    "message",
                    params["message"],
                    room=int(params["room"]),
                    namespace="/",
                )
            ch.basic_ack(method.delivery_tag)

        message_broker = RabbitMQService("chat_messages")
        message_broker.consume(callback)


@socketio.on("listen_message_broker")
def listen_message_broker(json):
    thread = Thread(target=consumer, args=(current_app._get_current_object(),))
    thread.daemon = True
    thread.start()


@socketio.on("left")
def left(json):
    room = session.get("chatroom_id")
    leave_room(room)
    emit("status", {"msg": current_user.username + " has left the room."}, room=room)
