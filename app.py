import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)

# This allows Vercel to talk to Render without any "Security Blocks"
CORS(app, resources={r"/*": {"origins": "*"}})

MONGO_URI = "mongodb+srv://Shravan67:shravan123@cluster0.dojp0db.mongodb.net/animal_charity?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client['animal_charity']

# Change the name slightly to 'get-data' to avoid any caching or path confusion
@app.route('/get-data', methods=['GET', 'OPTIONS'])
def get_contacts():
    if request.method == 'OPTIONS':
        return '', 200
    try:
        contacts = list(db.contacts.find({}, {'_id': 0}))
        return jsonify(contacts)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# TEMPORARILY COMMENT OUT THE HOMEPAGE
# If the URL is wrong now, you will get a 404 Error instead of "Backend is Running"
# This helps us find the real problem.
# @app.route('/')
# def home():
#     return "Backend is Running", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
