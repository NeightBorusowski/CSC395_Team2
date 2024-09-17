# app.py
from flask import Flask, render_template, request, jsonify

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

    #returns the data, format as needed
    return company, ingredients, llm

#add function to send data to llm and receive back response

#add function to send data returned from llm to frontend

    #hosts the website locally
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)