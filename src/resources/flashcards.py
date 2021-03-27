from datetime import datetime

from flask import jsonify, request
from flask_restful import abort
import flask_praetorian

from ..config import app, db
from ..models import FlashCardModel
from ..schemas import FlashCardSchema


# GET all method
@app.route('/flashcards', methods=['GET'])
@flask_praetorian.auth_required
def flashcard_list_get():
    flashcards = FlashCardModel.query.filter_by(user_id=flask_praetorian.current_user().id)
    return jsonify(FlashCardSchema(many=True).dump(flashcards))


# GET all by id
@app.route('/flashcards/<int:flashcards_id>', methods=['GET'])
@flask_praetorian.auth_required
def flashcard_get(flashcards_id):
    result = FlashCardModel.query.filter_by(id=flashcards_id, user_id=flask_praetorian.current_user().id).first()
    if not result:
        abort(404, message='Could not find Note with that ID')
    return jsonify(FlashCardSchema().dump(result))


# POST one, not limited by id
@app.route('/flashcards', methods=['POST'])
@flask_praetorian.auth_required
def flashcard_post():
    flashcard = FlashCardSchema().load(request.json)
    flashcard = FlashCardModel(**flashcard)
    flashcard.user_id = flask_praetorian.current_user().id
    db.session.add(flashcard)
    db.session.commit()
    return jsonify(FlashCardSchema().dump(flashcard)), 201


@app.route('/flashcards/<int:flashcards_id>', methods=['PATCH'])
@flask_praetorian.auth_required
def flashcard_patch(flashcards_id):
    flashcard = FlashCardSchema(partial=True).load(request.json)
    result = FlashCardModel.query.filter_by(id=flashcards_id, user_id=flask_praetorian.current_user().id).first()
    if not result:
        abort(404, message='Flashcard does not exist, cannot update')
    for key, value in flashcard.items():
        setattr(result, key, value)
    db.session.commit()
    return jsonify(FlashCardSchema().dump(result))


@app.route('/flashcards/<int:flashcards_id>/answers', methods=['PUT'])
@flask_praetorian.auth_required
def flashcard_put_answers(flashcards_id):
    result = FlashCardModel.query.filter_by(id=flashcards_id, user_id=flask_praetorian.current_user().id).first()
    if not result:
        abort(404, message='Flashcard does not exist, cannot answer')
    if request.json['correct']:
        result.date_viewed = datetime.now()


@app.route('/flashcards/<int:flashcards_id>', methods=['DELETE'])
@flask_praetorian.auth_required
def flashcard_delete(flashcards_id):
    result = FlashCardModel.query.filter_by(id=flashcards_id, user_id=flask_praetorian.current_user().id).first()
    if not result:
        abort(404, message='Flashcard does not exist, cannot delete')
    db.session.delete(result)
    db.session.commit()
    return '200'

# dump from database
# NoteSchema load from user
