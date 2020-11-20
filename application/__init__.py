from flask import Flask
from application.config import Config

app = Flask(__name__)
app.config.from_object(Config)

from application import routes