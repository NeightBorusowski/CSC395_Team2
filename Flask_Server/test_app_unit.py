import unittest
from unittest.mock import patch, MagicMock
from venv import create
from flask import Flask, jsonify
import json
import requests
from app import app, create_question, generate_ollama_response, get_gpt_response, get_mistral_response


class TestCases(unittest.TestCase):
    # the method below creates a test client for Flask
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.generate_ollama_response')
    def test_create_question(self, mock_generate_ollama_response):
        # mocks Ollama API response
        mock_generate_ollama_response.return_value = "Recipe from Ollama"

        company = "Test Company"
        ingredients = ["cheese, pasta"]
        llm = "Ollama"

        response = create_question(company, ingredients, llm)
        self.assertEqual(response, "Recipe from Ollama")

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
        mock_instance.chat.assert_called_once_with(model="llama2", messages=[{"role": "user", "content": question}],
                                                   stream=True)

    @patch('app.generate_ollama_response') # this decorator mocks the Ollama API call
    def test_submit_data_successful_request(self, mock_generate_ollama_response):
        # mock a successful response from Ollama API
        mock_generate_ollama_response.return_value = "Sample recipe response from LLM."

        sample = {
            "company": "Sample Company",
            "ingredients": "bread, meat, cheese",
            "llm": "Ollama"
        }

        # below is making a post request to /submit_data, json.dumps converts the sample to json string
        response = self.app.post('/submit_data', data = json.dumps(sample), content_type = 'application/json')

        # making several assertions to make sure the response is as expected. status_code 200 = success
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"status": "success", "response": "Sample recipe response from LLM."})

    def test_submit_data_invalid_request(self):
        sample = {
            "company": "Sample Company"
        }

        response = self.app.post('/submit_data', data = json.dumps(sample), content_type = 'application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"status": "error", "message": "Invalid request, 'company' and 'ingredients' are required"})

    @patch('app.requests.post')  # mocks requests.post
    def test_get_gpt_response_success(self, mock_gpt):
        # below simulates successful API response, with the return value
        # modelling API response format
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"choices": [{"message": {"content": "Sample response from ChatGPT."}}]}
        mock_gpt.return_value = mock_response

        question = "Sample question"
        api_key = "mock_api_key"
        response = get_gpt_response(question, api_key)

        self.assertEqual(response, "Sample response from ChatGPT.")
        mock_gpt.assert_called_once()

    @patch('app.requests.post')
    def test_get_gpt_response_failure(self, mock_gpt):
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request"
        mock_gpt.return_value = mock_response

        question = "Sample question"
        api_key = "mock_api_key"
        response = get_gpt_response(question, api_key)

        self.assertEqual(response, "Error: 400, Bad Request")
        mock_gpt.assert_called_once()

    @patch('app.requests.post')  # mocks post
    def test_get_gpt_response_authentication_error(self, mock_gpt):

        mock_gpt.return_value.status_code = 401
        mock_gpt.return_value.text = "Unauthorized"

        question = "Sample question"
        api_key = "mock_api_key"
        response = get_gpt_response(question, api_key)

        self.assertEqual(response, "Error: 401, Unauthorized")

    @patch('app.requests.post')
    def test_get_gpt_response_network_error(self, mock_post):
        # below simulates a network error
        mock_post.side_effect = requests.exceptions.RequestException("Network error")

        question = "Sample question"
        api_key = "mock_api_key"

        # below checks if network error is raised correctly
        with self.assertRaises(requests.exceptions.RequestException):
            get_gpt_response(question, api_key)

    @patch('app.requests.post')
    def test_get_mistral_response_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"choices": [{"message": {"content": "Sample Mistral response"}}]}
        mock_post.return_value = mock_response

        question = "Sample question"
        response = get_mistral_response(question)

        self.assertEqual(response, "Sample Mistral response")
        mock_post.assert_called_once()

    @patch('app.requests.post')
    def test_get_mistral_response_error(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request"
        mock_post.return_value = mock_response

        question = "Sample question"
        response = get_mistral_response(question)

        self.assertEqual(response, "Error: 400, Bad Request")
        mock_post.assert_called_once()

    @patch('app.requests.post')
    def test_get_mistral_response_network_error(self, mock_post):
        # below simulates a network error
        mock_post.side_effect = requests.exceptions.RequestException("Network error")

        question = "Sample question"

        # below checks if network error is raised correctly
        with self.assertRaises(requests.exceptions.RequestException):
            get_mistral_response(question)

if __name__ == '__main__':
    unittest.main()
