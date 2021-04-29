from flask_wtf import FlaskForm
from wtforms import RadioField, StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea


class Form(FlaskForm):
    collection = RadioField(
        'Collection Selection',
        choices=[
            'movies_incorrect',
            'nobel_prizes_incorrect'
        ]
    )
    query = StringField('Query')
    search = SubmitField('Search')
    editor = StringField('Editor', widget=TextArea())
    save = SubmitField('Save')
