from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from predictions import prediction

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains by default, can be restricted later if needed.


@app.route('/')
def home():
    return jsonify({"message": "Welcome to Flask API"})


@app.route('/app/data', methods=['GET', 'POST'])
@cross_origin(origins="http://localhost:5173")  # Allow only requests from React frontend
def handle_data():
    if request.method == 'POST':
        form_data = request.json
        sorted_keys = sorted(form_data.keys())
        data_store = []

        sorted_data = [form_data[key] for key in sorted_keys]

        data_store.append(sorted_data)
        output = prediction(data_store[0])[0]  # Call to the prediction function
        output = int(output)
        message = ""
        if output:
            message = "You have to readmit again"
        else:
            message = "You don't have to readmit"
            
        response_data = {
            "message": "Data received and processed successfully.",
            "success": True,
            "data": message
        }
        return jsonify(response_data)

    # If it's a GET request, send some sample data back
    sample_data = {
        "id": 1,
        "name": "Flask-React Integration",
        "description": "This is sample data from Flask to React."
    }
    return jsonify(sample_data)


if __name__ == "__main__":
    # Don't use app.run() for production, this is for dev purposes
    app.run(debug=True, port=5000)
