from flask import Flask, request, jsonify

app = Flask(__name__)
def recievedata(company, ingredients):
    print(f"company {company} ingredients {ingredients}")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)