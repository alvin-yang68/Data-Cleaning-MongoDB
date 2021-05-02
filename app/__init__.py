from flask import Flask
from flask_codemirror import CodeMirror

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
codemirror = CodeMirror(app)

from app import routes