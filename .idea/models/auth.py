from flask import request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash

# ✅ Signup function
def signup_user():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not (username and email and password):
        return jsonify({"error": "All fields are required"}), 400

    mongo = current_app.mongo
    existing_user = mongo.users.find_one({"email": email})
    if existing_user:
        return jsonify({"error": "User already exists"}), 409

    hashed_password = generate_password_hash(password)

    mongo.users.insert_one({
        "usern  ame": username,
        "email": email,
        "password": hashed_password
    })

    return jsonify({"message": "User registered successfully"}), 201

# ✅ Login function
def login_user():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not (email and password):
        return jsonify({"error": "Email and password are required"}), 400

    mongo = current_app.mongo
    user = mongo.users.find_one({"email": email})
    
    if not user:
        return jsonify({"error": "User not found"}), 404

    if not check_password_hash(user["password"], password):
        return jsonify({"error": "Incorrect password"}), 401

    return jsonify({"message": "Login successful", "username": user["username"]}), 200