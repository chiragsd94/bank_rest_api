from datetime import datetime

def calculate_updated_emi(loan):
    total_paid = sum(payment.amount for payment in loan.payments)
    remaining_principal = loan.principal - total_paid

    # Months passed since loan creation
    now = datetime.utcnow()
    months_passed = (now.year - loan.created_at.year) * 12 + (now.month - loan.created_at.month)
    remaining_months = max(loan.period_months - months_passed, 1)

    # Monthly interest rate
    r = loan.interest_rate / 100 / 12

    P = remaining_principal
    n = remaining_months

    # EMI formula
    if r > 0:
        emi = (P * r * (1 + r) ** n) / ((1 + r) ** n - 1)
    else:
        emi = P / n

    return round(emi, 2), remaining_principal, remaining_months
