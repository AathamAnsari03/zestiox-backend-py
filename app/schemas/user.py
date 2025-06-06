from marshmallow import Schema, fields

class UserRegisterSchema(Schema):
    name = fields.Str(required=True)
    mobile = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    mobile = fields.Str()
    created_at = fields.DateTime()
