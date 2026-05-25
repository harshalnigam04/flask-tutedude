from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
import json
import os

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["tutedude_db"]

# Load data from JSON file for /api route
def load_api_data():
    with open(os.path.join(os.path.dirname(__file__), 'data.json'), 'r') as f:
        return json.load(f)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api")
def api():
    return jsonify(load_api_data())

@app.route("/todo")
def todo():
    return render_template("todo.html")

@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():
    """
    Accepts itemName and itemDescription via POST request.
    Stores these details in MongoDB database.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    item_name = data.get("itemName")
    item_description = data.get("itemDescription")

    if not item_name:
        return jsonify({"error": "itemName is required"}), 400
    if not item_description:
        return jsonify({"error": "itemDescription is required"}), 400

    todo_item = {
        "itemName": item_name,
        "itemDescription": item_description
    }

    result = db.todos.insert_one(todo_item)
    return jsonify({
        "message": "Todo item stored successfully",
        "id": str(result.inserted_id),
        "itemName": item_name,
        "itemDescription": item_description
    }), 201

if __name__ == "__main__":
    app.run(debug=True)
