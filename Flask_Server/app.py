# app.py
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

# Get data from frontend 
@app.route("/submit_data", methods=["POST"])
def submit_data():
    data = request.get_json()  # Get the JSON data sent from the frontend

    # Validate incoming data
    if not data or 'company' not in data or 'ingredients' not in data:
        return jsonify({"status": "error", "message": "Invalid request, 'company' and 'ingredients' are required"}), 400

    # Store data in variables
    company = data.get('company')
    ingredients = data.get('ingredients')
    llm = data.get('llm', 'llama2')  # Optional field with default model

    # Process the received data
    question_response = create_question(company, ingredients)
    
    # Return the response from Ollama or handle failure
    return return_data(question_response)

# Function to send data to LLM and receive a response
def create_question(company, ingredients):
    # Formatting the question
    question = f"Create me a recipe using the company, {company} with these ingredients, {ingredients}"

    # Sending the question to the Ollama container
    ollama_response = send_to_ollama(question)

    # Returning the response
    return ollama_response

def send_to_ollama(question):
    # Define Ollama container's endpoint (running on port 11434)
    ollama_url = "http://ollama-container:11434/generate"  # Updated to http and localhost

    # Prepare payload for the POST request
    payload = {"prompt": question}

    try:
        response = requests.post(ollama_url, json=payload)
        response.raise_for_status()  # Raise error if the status code is not 200
        return response.json()  # Return the response from Ollama as a JSON object

    except requests.exceptions.HTTPError as http_err:
        return {"error": f"HTTP error occurred: {http_err}"}
    except requests.exceptions.RequestException as req_err:
        return {"error": f"Failed to get a response from Ollama: {str(req_err)}"}

# This function sends data back to the frontend in JSON format
def return_data(ollama_response):
    # Returns an error if the Ollama response is incorrect
    if "error" in ollama_response:
        return jsonify({"status": "error", "message": ollama_response["error"]}), 500

    # Send the Ollama response given that there has been no errors
    return jsonify({"status": "success", "data": ollama_response})

# Host the website locally
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
