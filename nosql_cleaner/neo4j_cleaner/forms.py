from flask_wtf import FlaskForm
from wtforms import RadioField, StringField, SubmitField
from flask_codemirror.fields import CodeMirrorField


class Form(FlaskForm):
    collection = RadioField(
        'Dataset Selection',
        choices=[
            'northwind',
        ],
        default='northwind'
    )
    query = StringField('Query')
    search = SubmitField('Search')
    editor = CodeMirrorField(language='javascript',
                             config={'lineNumbers': 'true'})
    save = SubmitField('Save')
