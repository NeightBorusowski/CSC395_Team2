# app.py
from flask import Flask, render_template, request, jsonify
#Tyler Test commit
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

#add function to send data to llm and receive back response

#add function to send data returned from llm to frontend


#hosts the website locally
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)