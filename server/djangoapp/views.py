# Uncomment the required imports before adding the code

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from datetime import datetime
from .models import CarMake, CarModel
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .populate import initiate
from .restapis import get_request, analyze_review_sentiments, post_review
from django.contrib.auth.decorators import login_required


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

def get_cars(request):
    count = CarMake.objects.filter().count()
    print(count)  # Debugging: Check the count in logs
    if count == 0:
        initiate()  # Populate the database if empty

    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car_model in car_models:
        cars.append({"CarModel": car_model.name, "CarMake": car_model.car_make.name})

    return JsonResponse({"CarModels": cars})

def get_dealerships(request, state="All"):
    if state == "All":
        endpoint = "/fetchDealers"
    else:
        endpoint = f"/fetchDealers/{state}"
    
    dealerships = get_request(endpoint)
    
    return JsonResponse({"status": 200, "dealers": dealerships})

# Create a `get_dealer_reviews` view to render the reviews of a dealer
def get_dealer_reviews(request, dealer_id):
    """Fetch reviews of a dealer by dealer_id and analyze sentiments."""
    endpoint = f"/fetchReviews/dealer/{dealer_id}"
    
    # Fetch reviews from backend API
    reviews = get_request(endpoint)

    if not reviews:
        return JsonResponse({"status": 404, "message": "No reviews found for this dealer."})

    analyzed_reviews = []
    
    for review in reviews:
        sentiment_result = analyze_review_sentiments(review["review"])
        sentiment = sentiment_result.get("label") if sentiment_result else "neutral"

        review_detail = {
            "id": review.get("id"),
            "name": review.get("name"),
            "dealership": review.get("dealership"),
            "review": review.get("review"),
            "purchase": review.get("purchase"),
            "purchase_date": review.get("purchase_date"),
            "car_make": review.get("car_make"),
            "car_model": review.get("car_model"),
            "car_year": review.get("car_year"),
            "sentiment": sentiment  # Add sentiment analysis result here
        }
        analyzed_reviews.append(review_detail)

    return JsonResponse({"status": 200, "reviews": analyzed_reviews})

# Create a `get_dealer_details` view to render the dealer details
def get_dealer_details(request, dealer_id):
    """Fetch details of a dealer by dealer_id."""
    endpoint = f"/fetchDealer/{dealer_id}"
    
    dealer_details = get_request(endpoint)

    return JsonResponse({"status": 200, "dealer": dealer_details})

# Create a `add_review` view to submit a review
@csrf_exempt
@login_required(login_url="/login")  # Ensure user authentication
def add_review(request):
    """Handles user review submission for a dealer."""
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Parse JSON request body

            # Call post_review function to send data to backend API
            response = post_review(data)

            # Return success if response is valid
            if response and response.get("id"):
                return JsonResponse({"status": 200, "message": "Review submitted successfully!"})

            return JsonResponse({"status": 401, "message": "Error in posting review"})

        except json.JSONDecodeError:
            return JsonResponse({"status": 400, "message": "Invalid JSON format"})

        except Exception as e:
            return JsonResponse({"status": 500, "message": str(e)})

    return JsonResponse({"status": 405, "message": "Invalid request method"})
