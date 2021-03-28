from datetime import datetime
from .config import db


class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True)
    password = db.Column(db.Text)
    roles = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)

    @property
    def rolenames(self):
        try:
            return self.roles.split(',')
        except Exception:
            return []

    @classmethod
    def lookup(cls, username):
        return cls.query.filter_by(username=username).one_or_none()

    @classmethod
    def identify(cls, id):
        return cls.query.get(id)

    @property
    def identity(self):
        return self.id

    def is_valid(self):
        return self.is_active


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
    date_due = db.Column(db.DateTime, nullable=True, default=datetime.now)


class FlashCardActivityModel(db.Model):
    __tablename__ = 'flashcard_activity'
    id = db.Column(db.Integer, primary_key=True)
    flashcards_id = db.Column(db.Integer, db.ForeignKey('flashcard.id'))
    date_reviewed = db.Column(db.DateTime, nullable=True)
    quality = db.Column(db.Integer, nullable=True)
    easiness = db.Column(db.Float)
    interval = db.Column(db.Integer)
    repetitions = db.Column(db.Integer)
    __mapper_args__ = {
        'order_by' : date_reviewed.desc()
    }