from flask_wtf import FlaskForm
from wtforms import RadioField, StringField, SubmitField
from wtforms.validators import DataRequired
from flask_codemirror.fields import CodeMirrorField


class MongoForm(FlaskForm):
    collection = RadioField(
        'Dataset Selection',
        choices=[
            'movies_incorrect',
            'nobel_prizes_incorrect'
        ]
    )
    query = StringField('Query')
    search = SubmitField('Search')
    editor = CodeMirrorField(language='javascript',
                             config={'lineNumbers': 'true'})
    save = SubmitField('Save')


class Neo4jForm(FlaskForm):
    collection = RadioField(
        'Dataset Selection',
        choices=[
            'northwind',
        ]
    )
    query = StringField('Query')
    search = SubmitField('Search')
    editor = CodeMirrorField(language='javascript',
                             config={'lineNumbers': 'true'})
    save = SubmitField('Save')
