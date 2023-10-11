from flask import (Blueprint, jsonify, request)
from v1.routes import db
from v1.models import Question
question_routes = Blueprint("routes.question", __name__)


@question_routes.route('/questions', methods=["POST"])
def post_question():
    if request.is_json:
        valid, errors = db.questions.is_valid(request.json)
        if not valid:
            return jsonify({
                "data": errors,
                "status": "error"
            }), 400
        # create question
        result = request.json
        user = db.users.query_by_field("email", result["user"])
        if not user:
            return jsonify({
                "message": "There is no user bearing an email {}".format(result["user"]),
                "status": "error"
            }), 400
        question = Question(
            user=user, subject=result["subject"], question=result["question"])
        db.questions.insert(question)
        if not user:
            return jsonify({
                "message": "User with that emmail address does not exist",
                "status": "error"
            }), 400
        return jsonify({
            "data": {
                "id": question.id,
                "user": question.user.first_name + " " + question.user.last_name,
                "subject": question.question,
                "question": question.question,
                "created_at": question.created_at,
                "updated_at": question.updated_at
            }
        }), 201
    else:
        return jsonify({
            "message": "Request should be in JSON",
            "status": "error"
        }), 400


@question_routes.route('/questions', methods=["GET"])
def get_questions():
    database = db.questions.query_all()
    result = []
    for data in database.values():
        result.append(data.to_json_object())
    return jsonify({
        "data": result,
        "status": "success"
    }), 200


@question_routes.route('/questions/<question_id>', methods=["GET"])
def get_question(question_id):
    question = db.questions.query_by_field("id", question_id)
    if question:
        return jsonify(question.to_json_object())
    response = {
        "message": "ivalid question id",
        "status": "error"
    }
    return jsonify(response), 400


@question_routes.route('/questions/<question_id>', methods=["DELETE"])
def delete_question(question_id):
    """Uses dictionary comprehension to remove an item with a given id"""
    question = db.questions.query_by_field("id", question_id)
    if not question:
        return jsonify({
            "message": "A question with that id does not exist",
            "status": "error"
        }), 400
    else:
        initial_length = len(db.questions.data)
        db.questions.data = {key: value for key, value in db.questions.data.items(
        ) if value.to_json_object()["id"] != question_id}
        if initial_length == len(db.questions.data):
            return jsonify({
                "message": "the question was not deleted",
                "status": "error"
            }), 400
        return jsonify({
            "data": question.to_json_object(),
            "status": "success"
        }), 200
