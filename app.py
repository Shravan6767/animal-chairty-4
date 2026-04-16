import os
from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

# PASTE YOUR ACTUAL CONNECTION STRING HERE
MONGO_URI = "mongodb+srv://your_username:your_password@cluster.mongodb.net/your_db"
client = MongoClient(MONGO_URI)
db = client['animal_charity'] # Use your actual DB name

@app.route('/api/admin/contacts', methods=['GET'])
def get_contacts():
    try:
        # This reaches into your 'contacts' collection
        contacts = list(db.contacts.find({}, {'_id': 0}))
        return jsonify(contacts)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Render needs this port binding to detect the 'open port'
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
