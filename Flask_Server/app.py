import openai

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
    ingredients = [data['ingredients']]
    llm = data.get('llm', 'llama2')
    try:
        question_response = create_question(company, ingredients)
        return jsonify({"status": "success", "response": question_response}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

def create_question(company, ingredients):
    #format question
    question = f"Create a recipe using the company {company} with these ingredients: {', '.join(ingredients)}."
    print(question)

    #sending question to Ollama
    return generate_ollama_response(question)

def generate_ollama_response(question):
    client = Client(host='http://host.docker.internal:11434')
    stream = client.chat(model="llama2", messages=[{"role": "user", "content": question}], stream=True)
    
    full_answer = ''
    for chunk in stream:
        full_answer += chunk['message']['content']
    print(full_answer)
    #return format_response(full_answer)
    return full_answer

def format_response(response):
    response = response.replace("```","")
    lines = response.split('\n')
    return '\n'.join(lines[1:-1])

#extra credit, generating a respone with chat gpt
openai.api_key = 'sk-9dNx3qA6CTN0IBfACuG0EzFsfGphGcbarbtFCBq5EzT3BlbkFJ5iUhxOi-dE_ffSBNJXycuyt9g9MM-rRPLNCrnm4zQA'

@app.route('/chatGPT', methods=['POST'])
def chatGPT():
    data1 = request.get_json()

    company1 = data1['company']
    ingredients1 = [data1['ingredients']]

    question1 = f"Create a recipe using the company {company1} with these ingredients: {', '.join(ingredients1)}."

    # Make the request to OpenAI API
    response = openai.Completion.create(
        engine="gpt-3.5-turbo",  # or "gpt-4", etc.
        prompt=question1,
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.7
    )

    # Get the response text from the OpenAI API
    gpt_response = response.choices[0].text.strip()
    print(gpt_response)


@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)