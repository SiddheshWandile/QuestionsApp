from flask import Flask, request, jsonify
from flask_cors import CORS
from models import init_db, register_user, validate_login, get_question_source

app = Flask(__name__)
CORS(app)
init_db(app)


@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    if register_user(username, password):
        return jsonify({"message": "User registered successfully"}), 201
    else:
        return jsonify({"error": "User registration failed"}), 500


@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if validate_login(username, password):
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"error": "Invalid credentials/Wrong UserName or Password"}), 401


@app.route('/api/question', methods=['POST'])
def get_question():
    data = request.json
    question_no = data.get('question_no')

    source_code = get_question_source(question_no)
    if source_code:
        return jsonify({
            "question_no": question_no,
            "source_code": source_code
        }), 200
    else:
        return jsonify({"error": "Question not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
