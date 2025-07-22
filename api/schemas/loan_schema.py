from marshmallow import Schema, fields

class LoanApplySchema(Schema):
    principal = fields.Float(required=True)
    interest_rate = fields.Float(required=True)
    period_years = fields.Int(required=True)


class LoanSchema(Schema):
    id = fields.Int()
    customer_id = fields.Int()
    principal = fields.Float()
    interest_rate = fields.Float()
    period_months = fields.Int()
    total_amount = fields.Float()
    emi_amount = fields.Float()
    created_at = fields.DateTime()

class PaymentSchema(Schema):
    loan_id = fields.Int(required=True)
    amount = fields.Float(required=True)
    type = fields.Str(required=False)
