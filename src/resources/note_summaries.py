from flask import jsonify
from flask_restful import abort

from ..config import app
from ..models import NoteModel
from ..schemas import NotesSchema
from .nlp_utils import generate_summary



@app.route('/note-summaries/<int:note_id>', methods=['GET'])
def notes_summaries_get(note_id):
    result = NoteModel.query.filter_by(id=note_id).first()
    if not result:
        abort(404, message='Could not find Note with that ID')
    summary = generate_summary(result.contents)
    data = {
            'finished': False,
            'name': 'Summary',
            'contents': summary
         }
    return jsonify(NotesSchema().dump(data))
