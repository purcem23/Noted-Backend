from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_apiexceptions import JSONExceptionHandler
from flask_login import LoginManager

app = Flask(__name__)
exception_handler = JSONExceptionHandler(app)
CORS(app)
login = LoginManager(app)
login.login_view = 'login'
api = Api(app)  # tells program wrap as api
# 'sqlite:///temp/database.db' to save to file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
