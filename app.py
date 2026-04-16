import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)

# UPDATED: This more aggressive CORS allows Vercel to talk to Render 
# without the "Preflight" check failing.
CORS(app, resources={r"/api/*": {"origins": "*"}})

# YOUR CONNECTION STRING
MONGO_URI = "mongodb+srv://Shravan67:shravan123@cluster0.dojp0db.mongodb.net/animal_charity?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client['animal_charity'] 

@app.route('/api/admin/contacts', methods=['GET', 'OPTIONS'])
def get_contacts():
    # This handles the "Preflight" request from the browser
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        # Reaching into your 'contacts' collection
        contacts = list(db.contacts.find({}, {'_id': 0}))
        return jsonify(contacts)
    except Exception as e:
        print(f"Database Error: {e}")
        return jsonify({"error": str(e)}), 500

# Added a basic root route so Render sees a '200 OK' when it pings your site
@app.route('/')
def home():
    return "Backend is Running", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
