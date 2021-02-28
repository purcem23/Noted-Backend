from datetime import datetime

from config import db


class NoteModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contents = db.Column(db.String(500), nullable=False)
    finished = db.Column(db.Boolean, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return f'Note(name = {self.name},' \
               f' contents ={self.contents},' \
               f' finished = {self.finished},' \
               f' date_created ={self.date_created} )'  # only shows when print/shown internally


class FlashCardModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    front = db.Column(db.String(150), nullable=False)
    back = db.Column(db.String(150), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    date_viewed = db.Column(db.DateTime, nullable=True)
    date_due = db.Column(db.DateTime, nullable=True)
    multiplier = db.Column(db.Integer, nullable=True)
