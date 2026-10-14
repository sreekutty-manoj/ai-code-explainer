from django.test import TestCase

# Create your tests here.

from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch
import requests

class ExplainCodeAPITests(APITestCase):

    def test_empty_code_returns_400(self):
        response = self.client.post(
            "/api/explain/",
            {"code": ""},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_whitespace_code_returns_400(self):
        response = self.client.post(
            "/api/explain/",
            {"code": "   "},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    @patch("code_explainer.views.requests.post")
    def test_valid_code_returns_200(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "response": "This function adds two numbers."
        }

        response = self.client.post(
            "/api/explain/",
            {"code": "def add(a, b): return a + b"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data["explanation"],
            "This function adds two numbers.",
        )

    
    @patch("code_explainer.views.requests.post")
    def test_ollama_connection_error_returns_503(self, mock_post):
        mock_post.side_effect = requests.exceptions.ConnectionError()

        response = self.client.post(
            "/api/explain/",
            {"code": "print(2 + 3)"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_503_SERVICE_UNAVAILABLE,
        )

