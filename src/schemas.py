from marshmallow import Schema, fields


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
    date_viewed = fields.DateTime(dump_only=True)
