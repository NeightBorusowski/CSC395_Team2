# app.py
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

def submit_data():
    data = request.get_json()  # Get the JSON data sent from the frontend

    company = data.get('company')
    ingredients = data.get('ingredients')
    llm = data.get('llm')

    # Process the received data
    print(f"Received data: Company: {company}, Ingredients: {ingredients}, LLM: {llm}")

    # Respond with a success message or further processing results
    return jsonify({'status': 'success', 'message': 'Data received successfully!'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)