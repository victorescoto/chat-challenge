from flask import Blueprint, redirect, url_for

main = Blueprint("main", __name__)

@main.route("/", methods=["GET"])
def index():
    return redirect(url_for("main.list_chatrooms"))

from . import auth_blueprint, chatroom_blueprint, events_blueprint
