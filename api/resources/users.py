from flask_smorest import Blueprint, abort
from flask_jwt_extended import create_access_token, get_jwt, jwt_required,get_jwt_identity
from flask.views import MethodView
from passlib.hash import pbkdf2_sha256

from api.models.Customer import Customer
from api.models.RevokedToken import RevokedToken
from api.schemas.user_schema import SignUpSchema,LoginSchema,CustomerSchema
from api.db import db

blp = Blueprint("Users", "users", description="Operations on users")

@blp.route("/signup")
class Signup(MethodView):
    @blp.arguments(SignUpSchema)
    def post(self, data):
        customer_data = data

        if Customer.query.filter_by(email=customer_data["email"]).first():
            abort(409, message="Email already exists")


        customer = Customer(
            name=customer_data["name"],
            email=customer_data["email"],
            password=pbkdf2_sha256.hash(customer_data["password"]),
            phone=customer_data["phone"],
            address=customer_data["address"],
            age=customer_data["age"],
            gender=customer_data["gender"]

        )
        
        db.session.add(customer)
        db.session.commit()
        return {"message": "User created successfully"}, 201
    

@blp.route("/login")
class Login(MethodView):
    @blp.arguments(LoginSchema)
    @blp.response(201, LoginSchema)
    def post(self, login_data):
        customer = Customer.query.filter_by(email=login_data["email"]).first()
        if customer and pbkdf2_sha256.verify(login_data["password"], customer.password):
            access_token = create_access_token(identity=str(customer.id))
            return {
                "access_token": access_token,
                "email": customer.email,
                "name": customer.name
            }, 201
        abort(401, message="Invalid email or password")


@blp.route("/logout")
class Logout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        revoked_token = RevokedToken(jti=jti)
        db.session.add(revoked_token)
        db.session.commit()
        return {"message": "Successfully logged out"}, 200
    

@blp.route("/profile")
class UserProfile(MethodView):
    @jwt_required()
    @blp.response(200, CustomerSchema)
    def get(self):
        user_id = get_jwt_identity()
        user = Customer.query.filter_by(id=user_id).first()
        if not user:
            abort(404, message="User not found")
        return user
