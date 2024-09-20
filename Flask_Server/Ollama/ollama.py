from flask import Flask, request, jsonify

app = Flask(__name__)

#nonfunctioning function used as example 
def recievedata(company, ingredients):
    print(f"company {company} ingredients {ingredients}")

#function that gets called in app.py, sends the question to this container
def send_to_ollama(question):




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)