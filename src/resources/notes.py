from flask import jsonify, request
from flask_restful import abort, reqparse
import flask_praetorian
import re
from ..config import app, db
from ..models import NoteModel, TagModel
from ..schemas import NotesSchema, TagSchema, McqSchema
from .nlp_utils import generate_summary
from .mcq_generation import (
    init_mcq,
    keyword_prep,
    keyword_to_sentence,
    generate_mcq,
)

note_put_args = reqparse.RequestParser()
note_put_args.add_argument(
    "name", type=str, help="Name of the Note is required", required=True
)
note_put_args.add_argument(
    "contents", type=str, help="Contents of the Note1", required=True
)
note_put_args.add_argument(
    "finished", type=bool, help="Is the note finished", required=True
)

note_update_args = reqparse.RequestParser()
note_update_args.add_argument(
    "name", type=str, help="Name of the Note is required"
)
note_update_args.add_argument(
    "contents", type=str, help="Contents of the Note2"
)
note_update_args.add_argument(
    "finished", type=bool, help="Is the note finished"
)


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
@app.route("/notes", methods=["GET"])
@flask_praetorian.auth_required
def notes_list_get():
    tag_name = request.args.get("tag")
    if tag_name:
        notes = NoteModel.query.filter(
            NoteModel.tags.any(name=tag_name),
            NoteModel.user_id == flask_praetorian.current_user().id,
        ).all()
    else:
        notes = NoteModel.query.filter(
            NoteModel.user_id == flask_praetorian.current_user().id
        ).all()
    return jsonify(NotesSchema(many=True).dump(notes))


# GET 1 by id
@app.route("/notes/<int:note_id>", methods=["GET"])
@flask_praetorian.auth_required
def notes_get(note_id):
    result = NoteModel.query.filter_by(
        id=note_id, user_id=flask_praetorian.current_user().id
    ).first()
    if not result:
        abort(404, message="Could not find Note with that ID")
    result.summary = generate_summary(result.contents)
    return jsonify(NotesSchema().dump(result))


# POST one, not limited by id
@app.route("/notes", methods=["POST"])
@flask_praetorian.auth_required
def notes_post():
    note = NotesSchema().load(request.json)
    note = NoteModel(**note)
    note.user_id = flask_praetorian.current_user().id
    # result = TagModel.query.filter_by(name='first_tag').first()
    # note.tags.append(result)
    matches = re.findall(r"\B(#[a-zA-Z0-9]+\b)", note.contents)
    matches += re.findall(r"\B(#[a-zA-Z0-9]+\b)", note.name)
    # remove old tags
    note.tags = []
    for match in matches:
        tag = get_or_create(db.session, TagModel, name=match[1:].lower())
        note.tags.append(tag)
        # create/find tag
        # add tag to notes
    db.session.add(note)
    db.session.commit()
    return jsonify(NotesSchema().dump(note)), 201


@app.route("/notes/<int:note_id>", methods=["PATCH"])
@flask_praetorian.auth_required
def notes_patch(note_id):
    note = NotesSchema(partial=True).load(request.json)
    result = NoteModel.query.filter_by(
        id=note_id, user_id=flask_praetorian.current_user().id
    ).first()
    if not result:
        abort(404, message="Note does not exist, cannot update")
    for key, value in note.items():
        setattr(result, key, value)
    matches = re.findall(r"\B(#[a-zA-Z0-9]+\b)", note["contents"])
    matches += re.findall(r"\B(#[a-zA-Z0-9]+\b)", note["name"])
    # remove old tags
    result.tags = []
    for match in matches:
        tag = get_or_create(db.session, TagModel, name=match[1:].lower())
        result.tags.append(tag)
        # create/find tag
        # add tag to notes
    db.session.commit()
    return jsonify(NotesSchema().dump(result))


@app.route("/notes/<int:note_id>", methods=["DELETE"])
@flask_praetorian.auth_required
def notes_delete(note_id):
    result = NoteModel.query.filter_by(
        id=note_id, user_id=flask_praetorian.current_user().id
    ).first()
    if not result:
        abort(404, message="Note does not exist, cannot de,ete")
    db.session.delete(result)
    db.session.commit()
    return "200"


@app.route("/notes/<int:note_id>/complete", methods=["PUT"])
@flask_praetorian.auth_required
def notes_completed(note_id):
    result = NoteModel.query.filter_by(
        id=note_id, user_id=flask_praetorian.current_user().id
    ).first()
    if not result:
        abort(404, message="Note does not exist, cannot update")
    result.finished = True
    db.session.commit()
    return jsonify(NotesSchema().dump(result))


@app.route("/notes/<int:note_id>/incomplete", methods=["PUT"])
@flask_praetorian.auth_required
def notes_incompleted(note_id):
    result = NoteModel.query.filter_by(
        id=note_id, user_id=flask_praetorian.current_user().id
    ).first()
    if not result:
        abort(404, message="Note does not exist, cannot update")
    result.finished = False
    db.session.commit()
    return jsonify(NotesSchema().dump(result))


# GET all method
@app.route("/tags", methods=["GET"])
@flask_praetorian.auth_required
def tags_list_get():
    tags = TagModel.query.filter_by()
    return jsonify(TagSchema(many=True).dump(tags))


@app.route("/notes_mcq/<int:note_id>", methods=["GET"])
@flask_praetorian.auth_required
def notes_mcq_get(note_id):
    result = NoteModel.query.filter_by(
        id=note_id, user_id=flask_praetorian.current_user().id
    ).first()
    if not result:
        abort(404, message="Could not find Note with that ID")
    summarized_text = init_mcq(result.contents)
    keyword_preparation = keyword_prep(result.contents, summarized_text)
    keyword_sentence_mapping = keyword_to_sentence(
        summarized_text, keyword_preparation
    )
    generated_mcq = generate_mcq(keyword_sentence_mapping)
    # import pdb; pdb.set_trace()
    return jsonify(McqSchema(many=True).dump(generated_mcq))


# dump from database
# NoteSchema load from user
