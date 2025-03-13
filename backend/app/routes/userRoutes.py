from flask import Blueprint, request, jsonify
from app.services.userService import UserService

user_bp = Blueprint("user", __name__)

@user_bp.route("/register", methods=["POST"])
def register_user():
    try:
        data = request.json
        user_id = UserService.register_user(data)
        return jsonify({"message": "User registered successfully", "user_id": user_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route("/<user_id>", methods=["GET"])
def get_user(user_id):
    user = UserService.get_user(user_id)
    if user:
        return jsonify(user), 200
    return jsonify({"message": "User not found"}), 404

@user_bp.route("/login", methods=["POST"])
def login_user():
    try:
        data = request.json
        user_id = UserService.authenticate_user(data["email"], data["password"])
        if user_id:
            return jsonify({"message": "Login successful", "user_id": user_id}), 200
        return jsonify({"error": "Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500
