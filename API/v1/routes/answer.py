from flask import (Blueprint, jsonify, request)
from v1.models import Answer
from v1.routes import db
answer_routes = Blueprint("routes.anwer", __name__)


@answer_routes.route('/questions/<question_id>/answers', methods=["POST"])
def answer_question(question_id):
    question = db.questions.query_by_field("id",question_id)
    if not question:
        return jsonify({
            "message": "invalid question id",
            "status": "error"
        }), 400
    if request.is_json:
        valid, errors = db.answers.is_valid(request.json)
        if not valid:
            return jsonify({
                "data": errors,
                "status": "error"
            }), 400
        result = request.json
        question = db.questions.query_by_field("id", question_id)
        user = db.users.query_by_field("email", result["user"])
        if not question:
            return jsonify({
                "message": "question id must be valid",
                "status": "error"
            }), 400
        if not user:
            return jsonify({
                "message": "the user email address provided does not exist",
                "status": "error"
            }), 400
        answer = Answer(
            user=user, question=question, answer=result["answer"])
        db.answers.insert(answer)
        return jsonify({
            "data": {
                "id": answer.id,
                "question": answer.question.question,
                "anwer": answer.answer,
                "user": answer.user.first_name + " "+answer.user.last_name
            },
            "status":"success"
        }), 201
    else:
        return jsonify({
            "message": "Request should be in JSON",
            "status": "error"
        }), 400
