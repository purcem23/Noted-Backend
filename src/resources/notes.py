from flask import jsonify, request
from flask_restful import abort, reqparse

from ..config import app, db
from ..models import NoteModel
from ..schemas import NotesSchema

note_put_args = reqparse.RequestParser()
note_put_args.add_argument('name', type=str, help='Name of the Note is required', required=True)
note_put_args.add_argument('contents', type=str, help='Contents of the Note1', required=True)
note_put_args.add_argument('finished', type=bool, help='Is the note finished', required=True)

note_update_args = reqparse.RequestParser()
note_update_args.add_argument('name', type=str, help='Name of the Note is required')
note_update_args.add_argument('contents', type=str, help='Contents of the Note2')
note_update_args.add_argument('finished', type=bool, help='Is the note finished')


# GET all method
@app.route('/notes', methods=['GET'])  # TODO change path to /notes
def notes_list_get():
    notes = NoteModel.query.all()
    return jsonify(NotesSchema(many=True).dump(notes))


# GET all by id
@app.route('/notes/<int:note_id>', methods=['GET'])
def notes_get(note_id):
    result = NoteModel.query.filter_by(id=note_id).first()
    if not result:
        abort(404, message='Could not find Note with that ID')
    return jsonify(NotesSchema().dump(result))


# POST one, not limited by id
@app.route('/notes', methods=['POST'])
def notes_post():
    note = NotesSchema().load(request.json)
    note = NoteModel(**note)
    db.session.add(note)  # add to current session
    db.session.commit()  # commit and make perm, otherwise it temp
    return jsonify(NotesSchema().dump(note)), 201  # 201 = created, 200 = ok(nothing broke)


@app.route('/notes/<int:note_id>', methods=['PATCH'])
def notes_patch(note_id):
    print(request.json)
    note = NotesSchema(partial=True).load(request.json)
    # note = NoteModel(**note)
    result = NoteModel.query.filter_by(id=note_id).first()
    if not result:
        abort(404, message='Note does not exist, cannot update')
    for key, value in note.items():
        setattr(result, key, value)
    db.session.commit()
    return jsonify(NotesSchema().dump(result))


@app.route('/notes/<int:note_id>', methods=['DELETE'])
def notes_delete(note_id):
    result = NoteModel.query.filter_by(id=note_id).first()
    db.session.delete(result)
    db.session.commit()
    return '200'


@app.route('/notes-completed/<int:note_id>', methods=['PUT'])
def notes_completed(note_id):
    print(request.json)
    result = NoteModel.query.filter_by(id=note_id).first()
    if not result:
        abort(404, message='Note does not exist, cannot update')
    result.finished = True
    db.session.commit()
    return jsonify(NotesSchema().dump(result))


# dump from database
# NoteSchema load from user
