from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity

from api.models.Bank import Loan, Payment
from api.models.Customer import Customer
from api.db import db
from api.schemas.loan_schema import LoanApplySchema, LoanSchema, PaymentSchema
from api.utils import calculate_updated_emi


blp = Blueprint("Loan", "loan", description="Loan related operations")


@blp.route("/apply")
class ApplyLoan(MethodView):
    @jwt_required()
    @blp.arguments(LoanApplySchema)
    def post(self, data):
        user_id = get_jwt_identity()
        customer = Customer.query.get(user_id)

        if not customer:
            abort(404, message="User not found")


        P = data["principal"]
        N = data["period_years"]
        R = data["interest_rate"]
        I = (P * N * R) / 100
        A = P + I
        emi = A / (N * 12)

        loan = Loan(
            customer_id=user_id,
            principal=P,
            interest_rate=R,
            period_months=N * 12,
            total_amount=A,
            emi_amount=emi
        )

        db.session.add(loan)
        db.session.commit()

        return {
            "message": "Loan applied successfully",
            "loan_id": loan.id,
            "customer_id": customer.id,
            "customer_name": customer.name,
            "customer_email": customer.email,
            "customer_phone": customer.phone,
            "customer_address": customer.address,
            "customer_age": customer.age,
            "customer_gender": customer.gender,
            "principal": P,
            "interest_rate": R,
            "period_years": N,
            "total_amount": A,
            "emi_amount": emi
        }, 201

@blp.route("/payments")
class LoanPayments(MethodView):
    @jwt_required()
    @blp.response(200, LoanSchema(many=True))
    def get(self):
        user_id = get_jwt_identity()
        customer = Customer.query.get(user_id)

        if not customer:
            abort(404, message="User not found")

        loans = Loan.query.filter_by(customer_id=user_id).all()

        if not loans:
            return {"message": "No loans found for this user"}, 404

        return loans

    @jwt_required()
    @blp.arguments(PaymentSchema)
    def post(self, payment_data):
        user_id = get_jwt_identity()
        loan_id = payment_data["loan_id"]

        loan = Loan.query.filter_by(id=loan_id, customer_id=user_id).first()
        if not loan:
            abort(404, message="Loan not found or unauthorized")


        payment = Payment(
            loan_id=loan.id,
            customer_id=user_id,
            amount=payment_data["amount"],
            type=payment_data.get("type", "lump-sum")
        )
        db.session.add(payment)

        new_emi, remaining_principal, _ = calculate_updated_emi(loan)
        loan.emi_amount = new_emi
        loan.total_amount = remaining_principal

        db.session.commit()

        return {
            "message": "Payment successful. EMI updated.",
            "new_emi": new_emi,
            "remaining_principal": remaining_principal
        }, 200

@blp.route("/ledger")
class LoanLedger(MethodView):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        customer = Customer.query.get(user_id)

        if not customer:
            abort(404, message="User not found")

        loans = Loan.query.filter_by(customer_id=user_id).all()

        ledger = []

        for loan in loans:
            payments = [
                {
                    "amount": p.amount,
                    "type": p.type,
                    "timestamp": p.timestamp
                }
                for p in loan.payments
            ]

            total_paid = sum(p["amount"] for p in payments)

            ledger.append({
                "loan_id": loan.id,
                "principal": loan.principal,
                "interest_rate": loan.interest_rate,
                "period_months": loan.period_months,
                "emi_amount": loan.emi_amount,
                "total_amount": loan.total_amount, 
                "created_at": loan.created_at,
                "total_paid": total_paid,
                "payments": payments
            })

        return {"ledger": ledger}, 200
