from flask import Flask, jsonify, request, render_template
import requests
from ollama import Client
import os

#constants
app = Flask(__name__)
api_key = "sk-SbQHK4vuxKgUg54j0RR1aJZd4VezN3eQCx0jn-dbrvT3BlbkFJFuU04r5n4fUa1M7d2zBL1xw_i9g5Y94FFYycgwuI8A"

@app.route("/submit_data", methods=["POST"])
def submit_data():
    data = request.get_json()

    # Validate incoming data
    if not data or 'company' not in data or 'ingredients' not in data:
        return jsonify({"status": "error", "message": "Invalid request, 'company' and 'ingredients' are required"}), 400

    company = data['company']
    ingredients = [data['ingredients']]
    llm = data.get('llm', 'llama2')

    try:
        question_response = create_question(company, ingredients, llm)
        return jsonify({"status": "success", "response": question_response}), 200 
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

def create_question(company, ingredients, llm):
    #format question
    question = f"Create a recipe using the company {company} with these ingredients: {', '.join(ingredients)}. Format as: title:, tagline:, then ingredients and recipe. ensure no newline between title and tagline, but always a newline between tagline and ingredients an recipe"
    print(question)

    #sending question to Ollama or any llm chosen
    if llm == "Ollama":
        return generate_ollama_response(question)
    elif llm == "ChatGPT":
        return get_gpt_response(question, api_key)
    elif llm == "Mistral":
        return get_mistral_response(question)

def generate_ollama_response(question):
    client = Client(host='http://host.docker.internal:11434')
    stream = client.chat(model="llama2", messages=[{"role": "user", "content": question}], stream=True)
    
    full_answer = ''
    for chunk in stream:
        full_answer += chunk['message']['content']
    return full_answer

#extra credit, generating a respone with chat gpt


def get_gpt_response(question, api_key):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "gpt-3.5-turbo",  # or "gpt-4" if you have access
        "messages": [{"role": "user", "content": question}],
        "max_tokens": 500,  # Adjust based on how long you want the response
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        response_data = response.json()
        return response_data['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code}, {response.text}"

def get_mistral_response(question):
    api_url = "https://api.mistral.ai/v1/chat/completions"
    key = ("IwvHistA7KPD7hEaUacofGx3QgSS9WNs")

    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistral-small-latest",
        "messages": [
            {"role": "user", "content": question}
        ],
        "max_tokens": 500
    }

    response = requests.post(api_url, headers = headers, json = data)

    if response.status_code == 200:
        response_data = response.json()
        return response_data["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code}, {response.text}"

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
   
    