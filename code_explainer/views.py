from django.shortcuts import render

# Create your views here.


import requests

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(["POST"])
def explain_code(request):
    # Get Python code from the incoming JSON request
    code = request.data.get("code")

    if not isinstance(code, str) or not code.strip():
        return Response(
            {"error": "Please provide non-empty Python code as text."},
            status=status.HTTP_400_BAD_REQUEST
        )
    prompt = f"""
    Explain this Python code in simple words.
    Give one example.

    Code:
    {code}
    """

    try:
        ollama_response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen2.5:0.5b",
                "prompt": prompt,
                "stream": False
            },
            timeout=180
        )

        ollama_response.raise_for_status()
        result = ollama_response.json()

        return Response({
            "code": code,
            "explanation": result["response"]
        })

    except requests.exceptions.ConnectionError:
        return Response(
            {"error": "Ollama is not running."},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )

    except requests.exceptions.Timeout:
        return Response(
            {"error": "The AI took too long to respond."},
            status=status.HTTP_504_GATEWAY_TIMEOUT
        )

    except requests.exceptions.RequestException:
        return Response(
            {"error": "Could not communicate with the AI model."},
            status=status.HTTP_502_BAD_GATEWAY
        )
