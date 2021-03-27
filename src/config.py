from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_apiexceptions import JSONExceptionHandler

app = Flask(__name__)
exception_handler = JSONExceptionHandler(app)
CORS(app)
api = Api(app)  # tells program wrap as api
# 'sqlite:///temp/database.db' to save to file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'top secret'
app.config['JWT_ACCESS_LIFESPAN'] = {'hours': 24}
app.config['JWT_REFRESH_LIFESPAN'] = {'days': 30}
db = SQLAlchemy(app)
