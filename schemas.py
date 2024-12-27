from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class CategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    is_global = fields.Bool(required=False, default=True)
    user_id = fields.Int(required=False, allow_none=True)

class RecordSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    category_id = fields.Int(required=True)
    timestamp = fields.DateTime(dump_only=True)
    amount = fields.Float(required=True)
