from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# This is where Ollama's API endpoint is
OLLAMA_MODEL_API = "http://ollama-container:11434/generate"  # Changed to avoid port conflict

@app.route('/generate', methods=['POST'])
def generate_response():
    # Getting the JSON data from the request
    data = request.get_json()

    # Validating the input data
    if not data or 'prompt' not in data:
        return jsonify({"error": "Invalid request, 'prompt' is required"}), 400

    # Extracting the prompt (question) from the incoming request
    question = data.get('prompt', '')

    # Sending the question to Ollama
    ollama_response = call_ollama_model(question)

    # Returning the response as JSON
    return jsonify({"response": ollama_response})

def call_ollama_model(prompt):
    # Prepare the payload for the Ollama model
    payload = {
        "model": "llama2",  # llama2 is the model we intend to use for this project
        "prompt": prompt
    }

    try:
        # Send a request to the Ollama model API
        response = requests.post(OLLAMA_MODEL_API, json=payload)

        # If response is successful and a response is generated, return the response
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('generated_text', 'No text generated')
        else:
            return f"Error: {response.status_code} - {response.text}"

    except requests.exceptions.RequestException as e:
        return f"Request to the Ollama model has failed: {e}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=11434)
