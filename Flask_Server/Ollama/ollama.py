from flask import Flask, request, jsonify, requests

app = Flask(__name__)

#nonfunctioning function used as example 
def recievedata(company, ingredients):
    print(f"company {company} ingredients {ingredients}")

#This is where ollama's API endpoint is
OLLAMA_MODEL_API = "http://localhost:5000/generate"

@app.route('/generate', methods=['POST'])
def generate_response():
    #Getting the JSON data from the request
    data = request.get_json()

    #extracting the prompt (question) from the incoming request
    question = data.get('prompt', '')

    #sending the question to ollama
    ollama_response = call_ollama_model(question)

    #returning the response as JSON
    return jsonify({"response": ollama_response})

def call_ollama_model(prompt):
    #prepare the payload for the ollama model
    payload = {
        "model": "llama2",  #llama2 is the model we intend to use for this project
        "prompt": prompt
    }

    try:
        #send a request to the ollama model API
        response = requests.post(OLLAMA_MODEL_API, json = payload)

        #if response is successful and a response is generated, return the response
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('generated_text', 'No text generated')
        else:
            return f"Error: {response.status_code} - {response.text}"

    except requests.exceptions.RequestException as e:
        return f"Request to the ollama model has failed: {e}"




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)