from app.services.message_service import MessageService
from flask import redirect, render_template, url_for
from flask_login import current_user, login_required
from sqlalchemy import exc

from ..forms import ChatroomForm
from ..serializers import ChatroomSchema
from ..services import ChatroomService
from . import main


@main.route("/chatrooms", methods=["GET"])
@login_required
def list_chatrooms():
    chatrooms = ChatroomService().list()
    return render_template("chatrooms/list.html", chatrooms=chatrooms)


@main.route("/chatrooms/<int:chatroom_id>", methods=["GET"])
@login_required
def show_chatroom(chatroom_id):
    chatroom = ChatroomService().get(chatroom_id)
    messages = MessageService().get_last_messages_by_chatroom(chatroom_id)
    messages.reverse()
    return render_template("chatrooms/show.html", chatroom=chatroom, messages=messages)


@main.route("/chatrooms/<int:chatroom_id>/delete", methods=["GET"])
@login_required
def delete_chatroom(chatroom_id):
    chatroom = ChatroomService().get(chatroom_id)

    if chatroom.author.id == current_user.id:
        ChatroomService().delete(chatroom)
    return redirect(url_for("main.list_chatrooms"))


@main.route("/chatrooms/create", methods=["GET", "POST"])
@login_required
def create_chatroom():
    form = ChatroomForm()

    if form.validate_on_submit():
        try:
            schema = ChatroomSchema()
            chatroom = schema.load(
                {"name": form.name.data, "author_id": current_user.id}
            )
            ChatroomService().save(chatroom)
        except exc.IntegrityError:
            form.name.errors.append("The chatroom name is already in use")
        else:
            return redirect(url_for("main.list_chatrooms"))

    return render_template("chatrooms/create.html", form=form)
