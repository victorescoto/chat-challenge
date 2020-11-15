from flask import redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user
from sqlalchemy import exc

from app.forms.login import LoginForm

from ..exceptions import UserNotFoundException
from ..forms import LoginForm, RegistrationForm
from ..models import User
from ..serializers import UserSchema
from ..services import UserService
from . import main


@main.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        try:
            user = User.query.filter_by(username=form.username.data).first()

            if user is None:
                raise UserNotFoundException()

            user.verify_password(form.password.data)
        except Exception:
            form.username.errors.append("Invalid credentials")
            form.password.errors.append("Invalid credentials")
        else:
            login_user(user)
            return redirect(url_for("main.list_chatrooms"))

    return render_template("auth/login.html", form=form)


@main.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.login"))


@main.route("/user", methods=["GET", "POST"])
def create_user():
    form = RegistrationForm()

    if form.validate_on_submit():
        try:
            user_schema = UserSchema()
            user = user_schema.load(
                {"username": form.username.data, "password": form.password.data}
            )
            user.hash_password()
            UserService().save(user)
        except exc.IntegrityError:
            form.username.errors.append("The username is already in use")
        else:
            return redirect(url_for("main.login"))

    return render_template("auth/register.html", form=form)
