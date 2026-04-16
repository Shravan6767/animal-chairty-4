import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)

# This is the most permissive CORS setting possible. 
# It tells the browser to allow EVERYTHING from ANYWHERE.
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})

# YOUR CONNECTION STRING
MONGO_URI = "mongodb+srv://Shravan67:shravan123@cluster0.dojp0db.mongodb.net/animal_charity?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client['animal_charity'] 

@app.route('/', methods=['GET', 'POST', 'OPTIONS'])
def home():
    return jsonify({"message": "Backend is Running"}), 200

@app.route('/api/admin/contacts', methods=['GET', 'POST', 'OPTIONS'])
def get_contacts():
    # Explicitly handle the 'Preflight' check
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        contacts = list(db.contacts.find({}, {'_id': 0}))
        return jsonify(contacts)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

@app.route('/api/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return '', 200
        
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Simple check for now - replace with your actual logic
    if username == "admin" and password == "admin123":
        return jsonify({"success": True, "message": "Login successful"}), 200
    else:
        return jsonify({"success": False, "message": "Invalid credentials"}), 401
