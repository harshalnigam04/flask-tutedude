from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["tutedude_db"]

# Sample data for /api route
api_data = {
    "project": "Tutedude Flask Project",
    "version": "1.0.0",
    "author": "harshalnigam04",
    "description": "A Flask project with REST API"
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api")
def api():
    return jsonify(api_data)

@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():
    data = request.get_json()
    item_name = data.get("itemName")
    item_description = data.get("itemDescription")
    if not item_name or not item_description:
        return jsonify({"error": "itemName and itemDescription are required"}), 400
    todo_item = {"itemName": item_name, "itemDescription": item_description}
    result = db.todos.insert_one(todo_item)
    return jsonify({"message": "Todo item stored successfully", "id": str(result.inserted_id)}), 201

if __name__ == "__main__":
    app.run(debug=True)
