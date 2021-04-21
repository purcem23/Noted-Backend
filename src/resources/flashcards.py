from datetime import datetime

from flask import jsonify, request
from flask_restful import abort
import flask_praetorian
import re
from ..config import app, db
from ..models import FlashCardModel, FlashCardActivityModel, TagModel
from ..schemas import FlashCardSchema, FlashCardAnswerSchema, TagSchema
from supermemo2 import first_review, SMTwo


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


# GET all method
@app.route('/flashcards', methods=['GET'])
@flask_praetorian.auth_required
def flashcard_list_get():
    tag_name = request.args.get('tag')
    if tag_name:
        flashcards = FlashCardModel.query.filter(FlashCardModel.tags.any(name=tag_name),
                                                 FlashCardModel.user_id == flask_praetorian.current_user().id).all()
    else:
        flashcards = FlashCardModel.query.filter(
            FlashCardModel.user_id == flask_praetorian.current_user().id).all()
    return jsonify(FlashCardSchema(many=True).dump(flashcards))


# GET all by id
@app.route('/flashcards/<int:flashcards_id>', methods=['GET'])
@flask_praetorian.auth_required
def flashcard_get(flashcards_id):
    result = FlashCardModel.query.filter_by(
        id=flashcards_id, user_id=flask_praetorian.current_user().id).first()
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
    matches = re.findall(r"\B(#[a-zA-Z0-9]+\b)", flashcard.front)
    matches += re.findall(r"\B(#[a-zA-Z0-9]+\b)", flashcard.back)
    # remove old tags
    flashcard.tags = []
    for match in matches:
        tag = get_or_create(db.session, TagModel, name=match[1:])
        flashcard.tags.append(tag)
        # create/find tag
        # add tag to notes
    db.session.add(flashcard)
    db.session.commit()
    return jsonify(FlashCardSchema().dump(flashcard)), 201


@app.route('/flashcards/<int:flashcards_id>', methods=['PATCH'])
@flask_praetorian.auth_required
def flashcard_patch(flashcards_id):
    flashcard = FlashCardSchema(partial=True).load(request.json)
    result = FlashCardModel.query.filter_by(
        id=flashcards_id, user_id=flask_praetorian.current_user().id).first()
    if not result:
        abort(404, message='Flashcard does not exist, cannot update')
    for key, value in flashcard.items():
        setattr(result, key, value)
    matches = re.findall(r"\B(#[a-zA-Z0-9]+\b)", flashcard['front'])
    matches += re.findall(r"\B(#[a-zA-Z0-9]+\b)", flashcard['back'])
    # remove old tags
    result.tags = []
    for match in matches:
        tag = get_or_create(db.session, TagModel, name=match[1:])
        result.tags.append(tag)
        # create/find tag
        # add tag to notes
    db.session.commit()
    return jsonify(FlashCardSchema().dump(result))


@app.route('/flashcards/<int:flashcards_id>', methods=['DELETE'])
@flask_praetorian.auth_required
def flashcard_delete(flashcards_id):
    result = FlashCardModel.query.filter_by(
        id=flashcards_id, user_id=flask_praetorian.current_user().id).first()
    if not result:
        abort(404, message='Flashcard does not exist, cannot delete')
    db.session.delete(result)
    db.session.commit()
    return '200'


@app.route('/flashcards/due', methods=['GET'])
@flask_praetorian.auth_required
def flashcards_due():
    flashcards = FlashCardModel.query.filter_by(
        user_id=flask_praetorian.current_user().id).filter(FlashCardModel.date_due <= datetime.now())
    return jsonify(FlashCardSchema(many=True).dump(flashcards))


@app.route('/flashcards/<int:flashcards_id>/answer', methods=['PUT'])
@flask_praetorian.auth_required
def flashcard_put_answers(flashcards_id):
    answer = FlashCardAnswerSchema().load(request.json)
    result = FlashCardModel.query.filter_by(
        id=flashcards_id, user_id=flask_praetorian.current_user().id).first()
    if not result:
        abort(404, message='Flashcard does not exist, cannot answer')
    previous = FlashCardActivityModel.query.filter_by(
        flashcards_id=flashcards_id)
    if previous.count() == 0:
        review = first_review(answer['score'], datetime.now())
        data = dict(
            flashcards_id=flashcards_id,
            quality=answer['score'],
            easiness=review._SMTwo__easiness,
            interval=review._SMTwo__interval,
            repetitions=review._SMTwo__repetitions,
            date_reviewed=datetime.now()
        )
        log = FlashCardActivityModel(**data)
        result.date_due = review._SMTwo__review_date
        db.session.add(log)
        db.session.commit()
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
        db.session.add(log)
        db.session.commit()
    return '200'


# dump from database
# NoteSchema load from user
