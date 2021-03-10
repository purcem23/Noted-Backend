from datetime import datetime

from flask import jsonify, request
from flask_restful import abort

from ..config import app, db
from ..models import FlashCardModel
from ..schemas import FlashCardSchema


# GET all method
@app.route('/flashcards', methods=['GET'])  # TODO change path to /notes
def flashcard_list_get():
    flashcards = FlashCardModel.query.all()
    return jsonify(FlashCardSchema(many=True).dump(flashcards))


# GET all by id
@app.route('/flashcards/<int:flashcards_id>', methods=['GET'])
def flashcard_get(flashcards_id):
    result = FlashCardModel.query.filter_by(id=flashcards_id).first()
    if not result:
        abort(404, message='Could not find Note with that ID')
    return jsonify(FlashCardSchema().dump(result))


# POST one, not limited by id
@app.route('/flashcards', methods=['POST'])
def flashcard_post():
    flashcards = FlashCardSchema().load(request.json)
    flashcards = FlashCardModel(**flashcards)
    db.session.add(flashcards)  # add to current session
    db.session.commit()  # commit and make perm, otherwise it temp
    return jsonify(FlashCardSchema().dump(flashcards)), 201  # 201 = created, 200 = ok(nothing broke)


@app.route('/flashcards/<int:flashcards_id>/answers', methods=['PUT'])
def flashcard_put_answers(flashcards_id):
    result = FlashCardModel.query.filter_by(id=flashcards_id).first()
    if request.json['correct']:
        result.date_viewed = datetime.now()


@app.route('/flashcards/<int:flashcards_id>', methods=['DELETE'])
def flashcard_delete(flashcards_id):
    result = FlashCardModel.query.filter_by(id=flashcards_id).first()
    db.session.delete(result)
    db.session.commit()
    return '200'

# dump from database
# NoteSchema load from user
