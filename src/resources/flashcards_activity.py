from datetime import datetime, date
from flask import jsonify, request
from flask_restful import abort

from ..config import app, db
from ..models import FlashCardActivityModel
from ..schemas import FlashCardActivitySchema
from supermemo2 import first_review

# GET all method
@app.route('/flashcards_activity', methods=['GET'])
def flashcard_activity_list_get():
    flashcards = FlashCardActivityModel.query.all()
    return jsonify(FlashCardActivitySchema(many=True).dump(flashcards))


# GET all by id
@app.route('/flashcards_activity/<int:flashcards_id>', methods=['GET'])
def flashcard_activity_get(flashcards_id):
    result = FlashCardActivityModel.query.filter_by(id=flashcards_id).first()
    if not result:
        abort(404, message='Could not find Note with that ID')
    return jsonify(FlashCardActivitySchema().dump(result))


# POST one, not limited by id
@app.route('/flashcards_activity', methods=['POST'])
def flashcard_activity_post():
    flashcards = FlashCardActivitySchema().load(request.json)
    flashcards = FlashCardActivityModel(**flashcards)
    db.session.add(flashcards)  # add to current session
    db.session.commit()  # commit and make perm, otherwise it temp
    return jsonify(FlashCardActivitySchema().dump(flashcards)), 201  # 201 = created, 200 = ok(nothing broke)


# supermemo2.first_review(quality, review_date=datetime.date.today())
#Calculates initial review date

# supermemo2.modify(instance,
#                   quality=None,
#                   easiness=None,
#                   interval=None,
#                   repetitions=None,
#                   review_date=None)
# modify any value from a previous value v

# calc(quality, easiness, interval, repetitions, review_date)
# calculates next date

#create new schema for var