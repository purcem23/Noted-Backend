from marshmallow import fields
from config import app, db
from models import NoteModel
import resources.notes
import resources.flashcards
import resources.note_summaries

# request import will allow info to be given over in {}

# db.create_all()


if __name__ == '__main__':
	app.run(debug=True)  # print out everything aka debug

# run main.py
