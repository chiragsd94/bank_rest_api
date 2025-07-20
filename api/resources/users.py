from flask_smorest import Blueprint, abort
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from flask.views import MethodView
from passlib.hash import pbkdf2_sha256

from api.models.Customer import Customer
from api.models.RevokedToken import RevokedToken
from api.schemas.user_schema import SignUpSchema,LoginSchema,UserSchema
from api.db import db

blp = Blueprint("Users", "users", description="Operations on users")

@blp.route("/signup")
class Signup(MethodView):
    @blp.arguments(SignUpSchema)
    @blp.response(201, SignUpSchema)
    def post(self, data):
        customer_data = data

        if Customer.query.filter_by(email=customer_data["email"]).first():
            abort(409, message="Email already exists")


        customer = Customer(
            name=customer_data["name"],
            email=customer_data["email"],
            password=pbkdf2_sha256(hash=customer_data["password"]),
            phone=customer_data["phone"],
            address=customer_data["address"],
            gender=customer_data["gender"]

        )
        
        db.session.add(customer)
        db.session.commit()
        return customer,201
    

@blp.route("/login")
class Login(MethodView):
    @blp.arguments(LoginSchema)
    @blp.response(201, LoginSchema)
    def post(self, login_data):
        customer = Customer.query.filter_by(email=login_data["email"]).first()
        if customer and pbkdf2_sha256.verify(login_data["password"], customer.password):
            access_token = create_access_token(identity=customer.id)
            return customer,200
        abort(401, message="Invalid email or password")


@blp.route("/logout")
class Logout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt_identity()
        revoked_token = RevokedToken(jti=jti)
        db.session.add(revoked_token)
        db.session.commit()
        return {"message": "Successfully logged out"}, 200
    

