# Uncomment the imports below before you add the function code
import os

import requests
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv("backend_url", default="http://localhost:3030")
sentiment_analyzer_url = os.getenv(
    "sentiment_analyzer_url", default="http://localhost:5050/"
)


def get_request(endpoint, **kwargs):
    params = ""
    if kwargs:
        params = "&".join([f"{key}={value}" for key, value in kwargs.items()])

    request_url = f"{backend_url}/{endpoint}?{params}"
    print(f"GET from {request_url}")

    try:
        # Call GET method of requests library with URL and parameters
        response = requests.get(request_url)
        return response.json()
    except requests.RequestException as e:
        # If any error occurs
        print(f"Network exception occurred: {e}")
        return None


# Add code for get requests to back end


def analyze_review_sentiments(text):
    request_url = sentiment_analyzer_url + "analyze/" + text
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(request_url)
        return response.json()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occurred")


def post_review(data_dict):
    """Sends a new dealer review to the backend API."""
    request_url = f"{backend_url}/insert_review"  # Backend API for posting reviews

    try:
        response = requests.post(request_url, json=data_dict)

        # If successful, return JSON response
        if response.status_code == 200 or response.status_code == 201:
            return response.json()
        else:
            return {
                "error": "Failed to post review",
                "status_code": response.status_code,
            }

    except Exception as err:
        print(f"Network exception occurred: {err}")
        return {"error": "Network exception occurred"}
