# app.py
from flask import Flask, jsonify
import requests
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

@app.route('create_question', methods='GET')
#function to send data to llm and receive back response
#test
def create_question():
    #temp variables to just try and get a response first before using the json
    var1 =  "Kraft"
    var2 = "Noodles and Cheese"

    #formatting the question
    question = f"Create me a recipe using the company {var1} with these ingredients, {var2}"

    #sending the question to the ollama container
    ollama_response = send_to_ollama(question)

    #returning the response
    return jsonify({"ollama's response:", ollama_response})








#add function to send data returned from llm to frontend


#hosts the website locally
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)