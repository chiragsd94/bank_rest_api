import os
from flask import Flask
from flask_smorest import Api
from dotenv import load_dotenv


#app specific imports
from api.db import db,migrate
from api.extension import cors,jwt_manager
from api.models.RevokedToken import RevokedToken

load_dotenv()


def create_app():
    app = Flask(__name__)
    
    #flask-smorest configurations
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "My API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["OPENAPI_JSON_PATH"] = "openapi.json"

    #flask-sqlalchemy configurations
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ECHO"] = True
    app.config["PROPAGATE_EXCEPTIONS"] = True

    #flask-cors configurations
    cors.init_app(app)
    
    #db initialization
    db.init_app(app)

    #flask-migrate configurations
    migrate.init_app(app, db)


    jwt_manager.init_app(app)

    # custom jwt token claims
    @jwt_manager.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        if RevokedToken.query.filter_by(jti=jti).first():
            return True
        return False

    @jwt_manager.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return {
            "description": "The token has been revoked",
            "error": "token_revoked",
        }, 401

    @jwt_manager.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return {"description": "The token has expired", "error": "token_expired"}, 401

    @jwt_manager.invalid_token_loader
    def invalid_token_callback(error):
        return (
            {"description": "Signature verification failed", "error": "invalid_token"},
        )
        401

    @jwt_manager.unauthorized_loader
    def unauthorized_callback(error):
        return {
            "description": "Authorization credentials are missing or incorrect",
            "error": "unauthorized",
        }, 401

    
    api = Api(app)
    return app