from marshmallow import Schema, fields, validate


class NotesSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.Str()
    contents = fields.Str()
    finished = fields.Boolean()
    date_created = fields.DateTime(dump_only=True)
    note_type = fields.Str()


class FlashCardSchema(Schema):
    id = fields.Integer(dump_only=True)
    front = fields.Str()
    back = fields.Str()
    date_created = fields.DateTime(dump_only=True)
    date_due = fields.DateTime(dump_only=True)

class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.Str()
    password = fields.Str()


class LoginSchema(Schema):
    username = fields.Str()
    password = fields.Str()


class FlashCardActivitySchema(Schema):
    flashcards_id = fields.Integer(dump_only=True)
    date_reviewed = fields.DateTime(dump_only=True)
    score = fields.Integer()


class FlashCardAnswerSchema(Schema):
    score = fields.Integer(validate=validate.OneOf([1, 2, 3, 4, 5]))
