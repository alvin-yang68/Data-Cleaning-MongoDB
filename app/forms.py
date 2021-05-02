from flask_wtf import FlaskForm
from wtforms import RadioField, StringField, SubmitField
from wtforms.validators import DataRequired
from flask_codemirror.fields import CodeMirrorField


class MongoForm(FlaskForm):
    collection = RadioField(
        'Dataset Selection',
        choices=[
            (1, 'movies_incorrect'),
            (2, 'nobel_prizes_incorrect')
        ],
        default=2
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
            (1, 'northwind'),
        ],
        default=1
    )
    query = StringField('Query')
    search = SubmitField('Search')
    editor = CodeMirrorField(language='javascript',
                             config={'lineNumbers': 'true'})
    save = SubmitField('Save')
