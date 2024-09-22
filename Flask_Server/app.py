# app.py
from flask import Flask, render_template, request, jsonify
import requests
#from Ollama.ollama import send_to_ollama
app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

#Get data from frontend 
@app.route("/submit_data", methods=["POST"])
def submit_data():
    data = request.get_json()  # Get the JSON data sent from the frontend

    #store data in variables
    company = data.get('company')
    ingredients = data.get('ingredients')
    llm = data.get('llm')

    # Process the received data
    # Pass the data to the function that handles the request to Ollama
    question_response = create_question(company, ingredients)
    
    # Return the response from Ollama or handle failure
    return return_data(question_response)

#function to send data to llm and receive back response
def create_question(company, ingredients):

    #formatting the question
    question = f"Create me a recipe using the company, {company} with these ingredients, {ingredients}"

    #sending the question to the ollama container
    ollama_response = send_to_ollama(question)

    #returning the response
    return ({"ollama_response": ollama_response})

def send_to_ollama(question):

    #Define Ollama container's endpoint (running on port 5000)
    ollama_url = "https://ollama_container:5000/generate"

    #send the formatted question to ollama using a POST request
    payload = {"prompt": question}

    try:
        response = requests.post(ollama_url, json=payload)
        response.raise_for_status()  # Raise error if the status code is not 200
        return response.json()  # Return the response from Ollama
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to get a response from Ollama: {str(e)}"}

# in this function I am sending data in json format to the frontend
def return_data(ollama_response):
    # returns an error if the ollama response is incorrect
    if "error" in ollama_response:
        # returns json object if there is an error using the flask jsonify method
        return jsonify({"status": "error", "message": ollama_response["error"]}), 500

    # send the ollama response given that there has been no errors in the response
    return jsonify({"status": "success", "data": ollama_response})

# hosts the website locally
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

