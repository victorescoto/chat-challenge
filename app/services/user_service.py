from flask import current_app
from ..models import User

class UserService():
    def get(self, id: int):
        ...

    def save(self, user: User):
        current_app.db.session.add(user)
        current_app.db.session.commit()
