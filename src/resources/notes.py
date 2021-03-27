from flask import jsonify, request
from flask_restful import abort, reqparse
import flask_praetorian

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
@flask_praetorian.auth_required
def notes_list_get():
    notes = NoteModel.query.filter_by(user_id=flask_praetorian.current_user().id)
    return jsonify(NotesSchema(many=True).dump(notes))


# GET all by id
@app.route('/notes/<int:note_id>', methods=['GET'])
@flask_praetorian.auth_required
def notes_get(note_id):
    result = NoteModel.query.filter_by(id=note_id, user_id=flask_praetorian.current_user().id).first()
    if not result:
        abort(404, message='Could not find Note with that ID')
    return jsonify(NotesSchema().dump(result))


# POST one, not limited by id
@app.route('/notes', methods=['POST'])
@flask_praetorian.auth_required
def notes_post():
    note = NotesSchema().load(request.json)
    note = NoteModel(**note)
    note.user_id = flask_praetorian.current_user().id
    db.session.add(note)
    db.session.commit()
    return jsonify(NotesSchema().dump(note)), 201


@app.route('/notes/<int:note_id>', methods=['PATCH'])
@flask_praetorian.auth_required
def notes_patch(note_id):
    note = NotesSchema(partial=True).load(request.json)
    result = NoteModel.query.filter_by(id=note_id, user_id=flask_praetorian.current_user().id).first()
    if not result:
        abort(404, message='Note does not exist, cannot update')
    for key, value in note.items():
        setattr(result, key, value)
    db.session.commit()
    return jsonify(NotesSchema().dump(result))


@app.route('/notes/<int:note_id>', methods=['DELETE'])
@flask_praetorian.auth_required
def notes_delete(note_id):
    result = NoteModel.query.filter_by(id=note_id, user_id=flask_praetorian.current_user().id).first()
    if not result:
        abort(404, message='Note does not exist, cannot de,ete')
    db.session.delete(result)
    db.session.commit()
    return '200'


@app.route('/notes/<int:note_id>/complete', methods=['PUT'])
@flask_praetorian.auth_required
def notes_completed(note_id):
    result = NoteModel.query.filter_by(id=note_id, user_id=flask_praetorian.current_user().id).first()
    if not result:
        abort(404, message='Note does not exist, cannot update')
    result.finished = True
    db.session.commit()
    return jsonify(NotesSchema().dump(result))


@app.route('/notes/<int:note_id>/incomplete', methods=['PUT'])
@flask_praetorian.auth_required
def notes_incompleted(note_id):
    result = NoteModel.query.filter_by(id=note_id, user_id=flask_praetorian.current_user().id).first()
    if not result:
        abort(404, message='Note does not exist, cannot update')
    result.finished = False
    db.session.commit()
    return jsonify(NotesSchema().dump(result))


# dump from database
# NoteSchema load from user
