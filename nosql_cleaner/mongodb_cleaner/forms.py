from flask_wtf import FlaskForm
from wtforms import RadioField, StringField, SubmitField
from flask_codemirror.fields import CodeMirrorField


class Form(FlaskForm):
    collection = RadioField(
        'Dataset Selection',
        choices=[
            'movies_incorrect',
            'nobel_prizes_incorrect'
        ],
        default='nobel_prizes_incorrect'
    )
    query = StringField('Query')
    search = SubmitField('Search')
    editor = CodeMirrorField(language='javascript',
                             config={'lineNumbers': 'true'})
    save = SubmitField('Save')
