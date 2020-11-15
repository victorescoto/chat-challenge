from flask_wtf import FlaskForm
from wtforms import StringField, validators

class ChatroomForm(FlaskForm):
    name = StringField("Name", [validators.Length(min=4, max=25)])
