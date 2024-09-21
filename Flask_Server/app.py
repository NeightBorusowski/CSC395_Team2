# app.py
from flask import Flask, render_template, request, jsonify, requests
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
    print(f"Received data: Company: {company}, Ingredients: {ingredients}, LLM: {llm}")

    # Respond with a success message or further processing results
    return jsonify({'status': 'success', 'message': 'Data received successfully!'})

#In this function, im creating a request to send to ollama.py (formatting a question with the variables to
#send too ollama.py)

@app.route("create_question", methods=["GET"])
#function to send data to llm and receive back response
def create_question():
    #temp variables to just try and get a response first before using the json
    var1 = "Kraft"
    var2 = "Noodles and Cheese"

    #formatting the question
    question = f"Create me a recipe using the company {var1} with these ingredients, {var2}"

    #sending the question to the ollama container
    ollama_response = send_to_ollama(question)

    #returning the response
    return jsonify({"ollama's response:", ollama_response})

def send_to_ollama(question):
    #Define Ollama container's endpoint (running on port 5000)
    ollama_url = "https://ollama_container:5000/generate"

    #send the formatted question to ollama using a POST request
    payload = {"prompt": question}
    response = requests.post(ollama_url, json = payload)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to get a response from ollama"}


#add function to send data returned from llm to frontend
def return_data(ollama_response):
    # returns an error if the ollama response is incorrect
    if "error" in ollama_response:
        return jsonify({"status": "error", "message": ollama_response["error"]}), 500

    # send the ollama response given that there has been no errors in the response
    return jsonify({"status": "success", "data": ollama_response})

# hosts the website locally
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)