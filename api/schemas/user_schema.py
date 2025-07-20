from marshmallow import Schema, fields

class SignUpSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(dump_only=True,required=True)
    phone = fields.Str(required=True)
    address = fields.Str(required=True)
    age = fields.Int(required=True)
    gender = fields.Str(required=True)

    


class LoginSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(dump_only=True,required=True)
    access_token = fields.Str()


class UserSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    email = fields.Str()
    phone = fields.Str()
    address = fields.Str()
    age = fields.Int()
    gender = fields.Str()
    loans=fields.List(fields.Nested('LoanSchema',many=True))
