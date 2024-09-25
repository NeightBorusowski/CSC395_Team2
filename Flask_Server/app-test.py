import unittest
from unittest.mock import patch, MagicMock
from venv import create

from flask import Flask, jsonify
import json
from app import app, create_question, generate_ollama_response

class MyTestCase(unittest.TestCase):
    # the method below creates a test client for Flask
    def testClient(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.generate_ollama_response') # this decorator mocks the Ollama API call
    def test_submit_data_successfully(self, mock_generate_ollama_response):
        # mock a successful response from Ollama API
        mock_generate_ollama_response.return_value = "Sample recipe response from LLM."

        sample = {
            "company": "Sample Company",
            "ingredients": "bread, meat, cheese"
            "llm": "llama2"
        }

        # below is making a post request to /submit_data
        response = self.app.post('/submit_data', data = json.dumps(sample), content_type = 'application/json')

        # making several assertions to make sure the response is as expected. status_code 200 = success
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['status'], 'success')
        self.assertEqual(response_data['response'], "Sample recipe response from LLM.")
        mock_generate_ollama_response.assert_called_once()

    def test_submit_data_invalid_request(self):
        sample = {
            "company": "Sample Company"
        }

        response = self.app.post('/submit_data', data = json.dumps(sample), content_type = 'application/json')

        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['status'], 'error')
        self.assertIn('Invalid request', response_data['message'])

    @patch('app.generate_ollama_response')
    def test_create_question(self, mock_generate_ollama_response):

        # mocks Ollama API response
        mock_generate_ollama_response.return_value = "Recipe from Ollama"

        company = "Test Company"
        ingredients = ["cheese, pasta"]
        response = create_question(company, ingredients)

        self.assertEqual(response, "Recipe from Ollama")
        mock_generate_ollama_response.assert_called_once_with("Create a recipe using the company 'Test Company' with these ingredients: cheese, pasta.")

    @patch('app.Client')
    def test_generate_ollama_response(self, mock_client):
        mock_instance = mock_client.return_value
        # below uses an iterator to handle data from ollama in chunks
        mock_instance.chat.return_value = iter([{"message": {"content": "Recipe part 1"}},
                                                {"message": {"content": " and part 2"}}])

    question = "Sample question"
    response = generate_ollama_response(question)

    # assertions
    self.assertEqual(response, "Recipe part 1 and part 2")
    mock_instance.chat.assert_called_once_with(model = "llama2", messages = [{"role": "user", "content": question}], stream = True)


if __name__ == '__main__':
    unittest.main()
