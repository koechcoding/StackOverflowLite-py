"""The main appication"""
from flask_jwt_extended import JWTManager
from v1.routes import db
from v1.routes.user import user_routes
from v1.routes.question import question_routes
from v1.routes.answer import answer_routes

def initialize_app(app):
    jwt = JWTManager(app)

    @jwt.token_in_blacklist_loader
    def check_token(token):
        """Check if token is blacklisted"""
        return token['jti'] in db.blacklist
    return app


def clear():
    """clear non-persistent data storage"""
    db.clear()
