from flask_smorest import Blueprint
from flask.views import MethodView

blp = Blueprint("About", "about", description="About related operations")

@blp.route("/")
class About(MethodView):
    def get(self):
        return {
            "disclaimer": {
                "summary": "This project is provided strictly for educational purposes only.",
                "details": [
                    "I am not liable for any financial loss, damage, or legal issues resulting from the use of this code.",
                    "I am not responsible for any misuse, unauthorized deployment, or abuse of this project in any environment.",
                    "I am not liable for any copyright or intellectual property claims that may arise from public usage.",
                    "This project is not intended to be used in production or for handling real financial transactions.",
                    "By using or modifying this code, you accept full responsibility for any consequences or issues that may arise.",
                    "This codebase is public solely for the purpose of demonstrating my Python and Flask REST API development skills to potential employers."
                ],
                "notice": "Use this project at your own risk. No guarantees or warranties are provided."
            },
            "project": {
                "name": "Bank REST API",
                "description": "A RESTful API for a fictional banking system built with Flask and Flask-Smorest. Supports user management, JWT auth, loan applications, payments, and a loan ledger.",
                "purpose": "Demonstration of backend development skills using Python, Flask, and modern API design."
            },
            "features": [
                "User registration, login, JWT-based authentication",
                "Loan application and repayment management",
                "Payment history and loan ledger tracking",
                "Swagger/OpenAPI auto-generated documentation",
                "Flask-Migrate for schema migrations",
                "CORS enabled for frontend interaction"
            ],
            "technology": {
                "language": "Python 3.12",
                "frameworks": ["Flask", "Flask-Smorest"],
                "orm": "Flask-SQLAlchemy",
                "migrations": "Flask-Migrate",
                "auth": "Flask-JWT-Extended",
                "env_management": "python-dotenv",
                "cors": "Flask-Cors"
            },
            "prerequisites": [
                "Python 3.12+",
                "pip",
                "PostgreSQL (or compatible DB)"
            ],
            "api_endpoints": [
                {"method": "POST", "path": "/api/v1/users/signup", "description": "Register a new user"},
                {"method": "POST", "path": "/api/v1/users/login", "description": "Authenticate and get JWT token"},
                {"method": "GET", "path": "/api/v1/users/profile", "description": "Get user profile (auth required)"},
                {"method": "POST", "path": "/api/v1/loans/apply", "description": "Apply for a loan (auth required)"},
                {"method": "POST", "path": "/api/v1/loans/payment", "description": "Make a payment (auth required)"},
                {"method": "GET", "path": "/api/v1/loans/payment", "description": "Get all loans (auth required)"},
                {"method": "GET", "path": "/api/v1/loans/ledger", "description": "View loan and payment ledger (auth required)"}
            ]
        }, 200
