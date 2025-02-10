# Uncomment the required imports before adding the code

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from datetime import datetime

from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
# from .populate import initiate


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    # Try to check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)

@csrf_exempt
def logout_request(request):
    if request.method == "GET":
        logout(request)  # ✅ Logs out the user
        return JsonResponse({"userName": ""}, status=200)
    
    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def registration(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            username = data.get("userName")
            password = data.get("password")
            first_name = data.get("firstName")
            last_name = data.get("lastName")
            email = data.get("email")

            if not username or not password or not first_name or not last_name or not email:
                return JsonResponse({"status": False, "error": "Missing fields"}, status=400)

            # Check if user already exists
            if User.objects.filter(username=username).exists():
                return JsonResponse({"status": False, "error": "Username already exists"}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({"status": False, "error": "Email already registered"}, status=400)

            # Create and save the user
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password, email=email)
            user.save()

            # Automatically log in the new user
            login(request, user)

            return JsonResponse({"status": True, "userName": user.username}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"status": False, "error": "Invalid JSON data"}, status=400)
        
        except Exception as e:
            return JsonResponse({"status": False, "error": str(e)}, status=500)

    return JsonResponse({"status": False, "error": "Invalid request method"}, status=405)

# # Update the `get_dealerships` view to render the index page with
# a list of dealerships
# def get_dealerships(request):
# ...

# Create a `get_dealer_reviews` view to render the reviews of a dealer
# def get_dealer_reviews(request,dealer_id):
# ...

# Create a `get_dealer_details` view to render the dealer details
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request):
# ...
