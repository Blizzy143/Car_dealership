# Uncomment the required imports before adding the code

import json
import logging

# from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# from django.http import HttpResponse, HttpResponseRedirect,
from django.http import JsonResponse

# from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt

from .models import CarMake, CarModel
from .populate import initiate
from .restapis import get_request, post_review
# from .restapis import analyze_review_sentiments

# from datetime import datetime


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data["userName"]
    password = data["password"]
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

            if (
                not username
                or not password
                or not first_name
                or not last_name
                or not email
            ):
                return JsonResponse(
                    {"status": False, "error": "Missing fields"}, status=400
                )

            # Check if user already exists
            if User.objects.filter(username=username).exists():
                return JsonResponse({
                    "status": False,
                    "error": "Username already exists"}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({
                    "status": False,
                    "error": "Email already registered"}, status=400)

            # Create and save the user
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=password,
                email=email,
            )
            user.save()

            # Automatically log in the new user
            login(request, user)

            return JsonResponse({
                "status": True,
                "userName": user.username}, status=201)

        except json.JSONDecodeError:
            return JsonResponse(
                {"status": False, "error": "Invalid JSON data"}, status=400
            )

        except Exception as e:
            return JsonResponse({"status": False, "error": str(e)}, status=500)

    return JsonResponse(
        {"status": False, "error": "Invalid request method"}, status=405
    )


def get_cars(request):
    count = CarMake.objects.filter().count()
    print(count)  # Debugging: Check the count in logs
    if count == 0:
        initiate()  # Populate the database if empty

    car_models = CarModel.objects.select_related("car_make")
    cars = []
    for car_model in car_models:
        cars.append({
            "CarModel": car_model.name,
            "CarMake": car_model.car_make.name})

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
    print(f"Fetching reviews for dealer ID: {dealer_id}")  # Debugging log
    endpoint = f"/fetchReviews/dealer/{dealer_id}"
    reviews = get_request(endpoint)

    print(f"Reviews Response: {reviews}")  # ✅ Add this debug log

    if reviews:
        return JsonResponse({"status": 200, "reviews": reviews})
    else:
        return JsonResponse({
            "status": 404,
            "error": "No reviews found"}, status=404)


# Create a `get_dealer_details` view to render the dealer details
def get_dealer_details(request, dealer_id):
    print(f"Fetching dealer details for ID: {dealer_id}")  # Debugging log
    endpoint = f"/fetchDealer/{dealer_id}"
    dealer = get_request(endpoint)

    if dealer and isinstance(dealer, dict):
        # ✅ Add debugging print statements
        print("Dealer API Response from Backend:", dealer)

        dealer["full_name"] = dealer.get(
            "full_name", f"{dealer.get('city', '')} {dealer.get('state', '')}"
        )

        return JsonResponse({"status": 200, "dealer": dealer})
    else:
        print("❌ Dealer API Response is empty or invalid")
        return JsonResponse({
            "status": 404,
            "error": "Dealer not found"}, status=404)


# Create a `add_review` view to submit a review
@csrf_exempt
@login_required(login_url="/login")  # Ensure user authentication
def add_review(request):
    """Handles user review submission for a dealer."""
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Parse JSON request body
            print("✅ Django Received Review Data:", data)  # Debugging log

            # Call post_review function to send data to Express
            response = post_review(data)

            print("📌 Express API Response:", response)  # ✅ Debugging log

            # Return success if response is valid
            if response and response.get("id"):
                return JsonResponse(
                    {
                        "status": 200,
                        "message": "Review submitted successfully!"
                    })

            return JsonResponse({
                "status": 401,
                "message": "Error in posting review"})

        except json.JSONDecodeError:
            return JsonResponse({
                "status": 400,
                "message": "Invalid JSON format"})

        except Exception as e:
            print("❌ Error in Django:", str(e))  # Debugging log
            return JsonResponse({"status": 500, "message": str(e)})

    return JsonResponse({"status": 405, "message": "Invalid request method"})
