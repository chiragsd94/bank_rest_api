from marshmallow import Schema, fields

class LoanSchema(Schema):
    id = fields.Str()
    loan_amount = fields.Str()
    loan_duration = fields.Str()
    loan_interest_rate = fields.Str()
    loan_status = fields.Str()
    loan_date = fields.Str()