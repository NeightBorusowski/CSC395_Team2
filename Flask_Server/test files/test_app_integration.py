import unittest
import json
from flask import Flask, jsonify
import requests

class TestIntegration(unittest.TestCase):
    def test_integration_with_server(self):
        url = 'http://127.0.0.1:5000/submit_data'
        headers = {'Content-Type': 'application/json'}

        payload = {
            'company': 'Nestle',
            'ingredients': 'cookies',
            'llm': 'Ollama'
        }

        response = requests.post(url, headers=headers, data=json.dumps(payload))

        self.assertEqual(response.status_code, 200)

        expected_response = "cookies"
        self.assertIn(expected_response, response.text)

if __name__ == '__main__':
    unittest.main()
