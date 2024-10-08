from flask import Flask, jsonify, request, render_template
import requests
from ollama import Client

#Constants
app = Flask(__name__)
api_key = "add APIKey here"

@app.route("/submit_data", methods=["POST"])
def submit_data():
    data = request.get_json()

    #Validate incoming data
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
    #Format question
    question = f"Create a recipe using the company {company} with these ingredients: {', '.join(ingredients)}. Format as: title:, tagline:, then ingredients and recipe. ensure no newline between title and tagline, but always a newline between tagline and ingredients an recipe"
    print(question)

    #Sending question to chosen LLM
    if llm == "Ollama":
        return generate_ollama_response(question)
    elif llm == "ChatGPT":
        return get_gpt_response(question, api_key)
    elif llm == "Mistral":
        return get_mistral_response(question)

#Ollama question
def generate_ollama_response(question):
    try:
        client = Client(host='http://host.docker.internal:11434')
        stream = client.chat(model="llama2", messages=[{"role": "user", "content": question}], stream=True)
    
        full_answer = ''
        for chunk in stream:
            if 'message' in chunk and 'content' in chunk['message']:
                full_answer += chunk['message']['content']
            else:
                return "Invalid response from Ollama"
        return full_answer
    except requests.exceptions.ConnectionError:
        return "Failed to connect to Ollama"

#ChatGPT question
def get_gpt_response(question, api_key):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "gpt-3.5-turbo",  #GPT model
        "messages": [{"role": "user", "content": question}],
        "max_tokens": 500, #Response length
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        response_data = response.json()
        return response_data['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code}, {response.text}"

    #Mistral Question
def get_mistral_response(question):
    api_url = "https://api.mistral.ai/v1/chat/completions"
    key = ("Add APIKEY here")

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
#render frontend
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
   
    
