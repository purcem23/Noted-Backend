from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from .config import db, login
from flask_login import UserMixin


@login.user_loader
def load_user(id):
    return UserModel.query.get(int(id))

class UserModel(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    notes = db.relationship('NoteModel', backref='author', lazy='dynamic')
    flashcards = db.relationship('FlashCardModel', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class NoteModel(db.Model):
    __tablename__ = 'note'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contents = db.Column(db.String(500), nullable=False)
    finished = db.Column(db.Boolean, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Note(name = {self.name},' \
               f' contents ={self.contents},' \
               f' finished = {self.finished},' \
               f' date_created ={self.date_created} )'  # only shows when print/shown internally


class FlashCardModel(db.Model):
    __tablename__ = 'flashcard'
    id = db.Column(db.Integer, primary_key=True)
    front = db.Column(db.String(150), nullable=False)
    back = db.Column(db.String(150), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_viewed = db.Column(db.DateTime, nullable=True)
    date_due = db.Column(db.DateTime, nullable=True)
    multiplier = db.Column(db.Integer, nullable=True)


