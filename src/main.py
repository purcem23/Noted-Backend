from marshmallow import fields
from .config import app, db
from .models import NoteModel
from .resources import notes, flashcards, note_summaries, users

# request import will allow info to be given over in {}

db.create_all()


if __name__ == '__main__':
	app.run(debug=True)  # print out everything aka debug

# run main.py
