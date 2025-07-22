from marshmallow import Schema, fields
from api.schemas.loan_schema import LoanSchema

class SignUpSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True)
    phone = fields.Str(required=True)
    address = fields.Str(required=True)
    age = fields.Str(required=True)
    gender = fields.Str(required=True)


class LoginSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(load_only=True,required=True)
    access_token = fields.Str()


class CustomerSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    email = fields.Str()
    phone = fields.Str()
    address = fields.Str()
    age = fields.Str()
    gender = fields.Str()
    loans = fields.List(fields.Nested(LoanSchema))


class PaymentSchema(Schema):
    id = fields.Int()
    loan_id = fields.Int()
    customer_id = fields.Int()
    amount = fields.Float()
    type = fields.Str()
    timestamp = fields.DateTime()
