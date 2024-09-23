from flask import Flask, jsonify, request, render_template
from ollama import Client

app = Flask(__name__)

@app.route("/submit_data", methods=["POST"])
def submit_data():
    data = request.get_json()

    # Validate incoming data
    if not data or 'company' not in data or 'ingredients' not in data:
        return jsonify({"status": "error", "message": "Invalid request, 'company' and 'ingredients' are required"}), 400

    company = data['company']
    ingredients = data['ingredients']
    llm = data.get('llm', 'llama2')  # Optional field with default model

    # Process the received data
    try:
        question_response = create_question(company, ingredients)
        return jsonify({"status": "success", "response": question_response}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

def create_question(company, ingredients):
    # Formatting the question
    question = f"Create a recipe using the company {company} with these ingredients: {', '.join(ingredients)}."

    # Sending the question to the Ollama container
    return generate_ollama_response(question)

def generate_ollama_response(question):
    client = Client(host='http://host.docker.internal:11434')
    stream = client.chat(model="llama2", messages=[{"role": "user", "content": question}], stream=True)
    
    full_answer = ''
    for chunk in stream:
        full_answer += chunk['message']['content']

    return full_answer.strip()  # Strip any leading/trailing whitespace

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
