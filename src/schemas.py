from marshmallow import Schema, fields, validate


class NotesSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.Str()
    contents = fields.Str()
    summary = fields.Str(dump_only=True)
    finished = fields.Boolean()
    date_created = fields.DateTime(dump_only=True)
    note_type = fields.Str()
    tags = fields.List(fields.Str(), dump_only=True)


class FlashCardSchema(Schema):
    id = fields.Integer(dump_only=True)
    front = fields.Str()
    back = fields.Str()
    date_created = fields.DateTime(dump_only=True)
    date_due = fields.DateTime(dump_only=True)
    tags = fields.List(fields.Str(), dump_only=True)


class TagStatSchema(Schema):
    tag = fields.Str(dump_only=True)
    score = fields.Number()
    repetitions = fields.Integer()


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.Str()
    password = fields.Str(load_only=True)


class LoginSchema(Schema):
    username = fields.Str()
    password = fields.Str()


class FlashCardAnswerSchema(Schema):
    score = fields.Integer(validate=validate.OneOf([0, 1, 2, 3, 4, 5]))


class TagSchema(Schema):
    name = fields.Str()


class McqSchema(Schema):
    question = fields.Str()
    answer = fields.Str()
    fake_answers = fields.List(fields.Str())
