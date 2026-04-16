import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)

# This is the "Open Door" policy. It tells the browser to allow EVERYTHING.
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

MONGO_URI = "mongodb+srv://Shravan67:shravan123@cluster0.dojp0db.mongodb.net/animal_charity?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client['animal_charity']

@app.route('/get-data', methods=['GET', 'OPTIONS'])
def get_contacts():
    if request.method == 'OPTIONS':
        return '', 200
    try:
        contacts = list(db.contacts.find({}, {'_id': 0}))
        return jsonify(contacts)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Keep this for Render's "Health Check"
@app.route('/')
def home():
    return "OK", 200

if __name__ == "__main__":
    # Render provides the PORT environment variable. We MUST use it.
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
