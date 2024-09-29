import unittest
from unittest.mock import patch, MagicMock
from venv import create
from flask import Flask, jsonify
import json
import requests
from app import app, create_question, generate_ollama_response
from app import get_gpt_response

class TestOllamaCases(unittest.TestCase):
    # the method below creates a test client for Flask
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.generate_ollama_response') # this decorator mocks the Ollama API call
    def test_submit_data_successfully(self, mock_generate_ollama_response):
        # mock a successful response from Ollama API
        mock_generate_ollama_response.return_value = "Sample recipe response from LLM."

        sample = {
            "company": "Sample Company",
            "ingredients": "bread, meat, cheese",
            "llm": "llama2"
        }

        # below is making a post request to /submit_data, json.dumps converts the sample to json string
        response = self.app.post('/submit_data', data = json.dumps(sample), content_type = 'application/json')

        # making several assertions to make sure the response is as expected. status_code 200 = success
        self.assertEqual(response.status_code, 200)
        # response_data takes the data and converts to python dictionary
        response_data = json.loads(response.data)
        self.assertEqual(response_data['status'], 'success')
        self.assertEqual(response_data['response'], "Sample recipe response from LLM.")
        # assert_called_once() object ensures the ollama response is called exactly one time
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
        mock_generate_ollama_response.assert_called_once_with("Create a recipe using the company Test Company with these ingredients: cheese, pasta.")

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

class TestGPTCases(unittest.TestCase):

    @patch('app.requests.post') # mocks requests.post
    def test_get_gpt_response_success(self, mock_post):
        # below simulates successful API response, with the return value
        # modelling API response format
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "choices": [
            {
                "message": {
                    "content": "This is a test response from GPT-3.5"
                }
            }
        ]
    }

        question = "What is the definition of AI?"
        api_key = "test-api-key"

        response = get_gpt_response(question, api_key)

        self.assertEqual(response, "This is a test response from GPT-3.5")

        # below checks proper URL, headers, data
        mock_post.assert_called_once_with("https://api.openai.com/v1/chat/completions",
                                          headers = {
                                              "Authorization": f"Bearer {api_key}",
                                              "Content-Type": "application/json",
                                          },
                                          json={
                                              "model": "gpt-3.5-turbo",
                                              "messages": [{"role": "user", "content": question}],
                                              "max_tokens": 500,
                                          }
                                          )

    @patch('app.requests.post')
    def test_get_gpt_response_api_error(self, mock_post):
        mock_post.return_value.status_code = 401
        mock_post.return_valaue.text = "Unauthorized"

        question = "What is the definition of AI?"
        api_key = "invalid-api-key"

        response = get_gpt_response(question, api_key)

        self.assertEqual(response, "Error: 401, Unauthorized")

    @patch('app.requests.post')
    def test_get_gpt_response_network_error(self, mock_post):
        # below simulates a network error
        mock_post.side_effect = requests.exceptions.RequestException("Network error")

        question = "What is the definition of AI?"
        api_key = "test-api-key"

        # below checks if network error is raised correctly
        with self.assertRaises(requests.exceptions.RequestException):
            get_gpt_response(question, api_key)

if __name__ == '__main__':
    unittest.main()
