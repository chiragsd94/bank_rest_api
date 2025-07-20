from api.db import db 
from datetime import datetime

class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
    principal = db.Column(db.Float, nullable=False)
    interest_rate = db.Column(db.Float, nullable=False)
    period_months = db.Column(db.Integer, nullable=False)
    total_amount = db.Column(db.Float)
    emi_amount = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    transactions = db.relationship("Transaction", backref="loan")
