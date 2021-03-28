from datetime import datetime

from flask import jsonify, request
from flask_restful import abort
import flask_praetorian

from ..config import app, db
from ..models import FlashCardModel, FlashCardActivityModel
from ..schemas import FlashCardSchema, FlashCardAnswerSchema
from supermemo2 import first_review, SMTwo

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



@app.route('/flashcard-answers/<int:flashcards_id>', methods=['PUT'])
def flashcard_put_answers(flashcards_id):
    answer = FlashCardAnswerSchema().load(request.json)
    result = FlashCardModel.query.filter_by(id=flashcards_id).first()
    previous = FlashCardActivityModel.query.filter_by(flashcards_id=flashcards_id)
    if previous.count() == 0:
        review = first_review(answer['score'], datetime.now())
        data = dict(
            flashcards_id = flashcards_id,
            quality=answer['score'],
            easiness=review._SMTwo__easiness,
            interval=review._SMTwo__interval,
            repetitions=review._SMTwo__repetitions,
            date_reviewed = datetime.now()
        )
        log = FlashCardActivityModel(**data)
        result.date_due = review._SMTwo__review_date
        db.session.add(log)  # add to current session
        db.session.commit()  # commit and make perm, otherwise it temp

    else:
        last_review = previous.first()
        review = SMTwo()
        review.calc(quality=last_review.quality,
                    easiness=last_review.easiness,
                    interval=last_review.interval,
                    repetitions=last_review.repetitions,
                    review_date=datetime.now())
        log = FlashCardActivityModel(
            flashcards_id=flashcards_id,
            quality=answer['score'],
            easiness=review._SMTwo__easiness,
            interval=review._SMTwo__interval,
            repetitions=review._SMTwo__repetitions,
            date_reviewed=datetime.now())
        result.date_due = review._SMTwo__review_date
        db.session.add(log)  # add to current session
        db.session.commit()  # commit and make perm, otherwise it temp
    return '200'


@app.route('/flashcards-due', methods=['GET'])
def flashcards_due(user_id):
    flashcards = db.session.query(FlashCardModel).filter(FlashCardModel.date_due <= datetime.now()) #, FlashCardModel.user_id == user_id)
    # flashcards = FlashCardModel.query.filter_by(id=user_id,date_due())
    return jsonify(FlashCardSchema(many=True).dump(flashcards))



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
