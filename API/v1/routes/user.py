from flask import (Blueprint, request, jsonify)
from v1.models import User
import json
from v1.routes import db
from passlib.hash import bcrypt
from flask_jwt_extended import (create_access_token, jwt_required, get_raw_jwt)
user_routes = Blueprint("routes.user", __name__)


@user_routes.route("/signup", methods=["POST"])
def register_user():
    if request.is_json:
        valid, errors = db.users.is_valid(request.json)
        if not valid:
            return jsonify({
                "data": errors,
                "status": "error"
            }), 400
        # create a user
        result = request.json
        user = User(result["first_name"], result["last_name"],
                    result["email"], result["password"])
        db.users.insert(user)
        return jsonify({
            "data": {
                "user": {
                    "id": user.id,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "password": user.password,
                    "created_at": user.created_at,
                    "updated_at": user.updated_at
                },
                "status": "success"
            }
        }), 201
    else:
        return jsonify({
            "message": "Request shold be in JSON",
            "status": "error"
        }), 400


@user_routes.route('/login', methods=["POST"])
def login_user():
    if request.is_json:
        if not request.json.get("email"):
            return jsonify({
                "status": "error",
                "data": {
                    "email": "Email is required"
                }
            }), 400
        if not request.json.get("password"):
            return jsonify({
                "status": "error",
                "data": {
                    "email": "password is required"
                }
            }), 400
        user = db.users.query_by_field("email", request.json.get("email"))
        if not user:
            return jsonify({
                "status": "error",
                "message": "email does not exist"
            }), 400
        elif not bcrypt.verify(request.json.get("password"), user.password):
            return jsonify({
                "status": "error",
                "message": "wrong password"
            }), 400
        access_token = create_access_token(identity=user.email)
        return jsonify({
            "status": "success",
            "data": {
                "token": access_token,
                "user": user.to_json_object()
            }
        }), 200
    else:
        return jsonify({
            "message": "Request should be in JSON",
            "status": "error"
        }), 400


@user_routes.route("/logout", methods=["DELETE"])
@jwt_required
def logout_user():
    jti = get_raw_jwt()['jti']
    db.blacklist.add(jti)
    return jsonify({
        "status": "success",
        "message": "successfuly logged out"
    })
