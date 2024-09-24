import unittest
from unittest.mock import patch, MagicMock
from flask import Flask, jsonify
import json
from app import app, create_question, generate_ollama_response

class MyTestCase(unittest.TestCase):
    def t(self):
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
