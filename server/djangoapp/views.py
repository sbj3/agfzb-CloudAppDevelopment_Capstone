from django.shortcuts import render
# from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
# from django.shortcuts import get_object_or_404, redirect
from .models import CarModel
# from .models import CarMake, CarDealer, DealerReview
from django.views import generic
# from django.views import View
# from .models import DealerReview
from .restapis import get_dealers_from_cf, get_dealer_by_id
from .restapis import get_dealer_reviews_from_cf
from .restapis import post_request
# from .restapis import get_dealers_by_state

from django.contrib.auth import login, logout, authenticate
# from django.contrib import messages
from datetime import datetime
import logging
# import json

# Get an instance of a logger
logger = logging.getLogger(__name__)
api_url = "https://us-south.functions.appdomain.cloud/api/v1/web/" + \
          "broadus.jones%40gmail.com_dev/api/"

# Create your views here.


def about(request):
    # Create an `about` view to render a static about page
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/about.html', context)


def contact(request):
    # Create a `contact` view to return a static contact page
    # def contact(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/contact.html', context)


# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            print("Log in from user '{}'".format(username))
            return render(request, 'djangoapp/index.html', context)
        else:
            print("Log in failed from user '{}'".format(username))
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/index.html', context)
    else:
        print("Log in request not using 'POST'")
        return render(request, 'djangoapp/index.html', context)


def logout_request(request):
    # Create a `logout_request` view to handle sign out request
    context = {}
    print("Log out the user '{}'".format(request.user.username))
    logout(request)
    return render(request, 'djangoapp/index.html', context)


def registration_request(request):
    # Create a `registration_request` view to handle sign up request
    # def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        # Check if user exists
        # Get user information from request.POST
        # username, first_name, last_name, password
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except Exception as err:
            # If not, simply log this is a new user
            logger.debug("{} is new user. Err: {}".format(username, err))
        if not user_exist:
            # Create user in austh_user table
            user = User.objects.create_user(
                username=username, password=password,
                first_name=first_name, last_name=last_name)
            # Login the user and
            # redirect to main page
            login(request, user)
            return render(request, 'djangoapp/index.html', context)
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)


def get_dealerships(request):
    """
    # Update the `get_dealerships` view to render the index page with a list
    # of dealerships
    # def get_dealerships(request):
    #     context = {}
    #     if request.method == "GET":
    #         return render(request, 'djangoapp/index.html', context)
    """
    context = {}
    if request.method == "GET":
        url = api_url + "dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        # dealer_names = [dealer.short_name for dealer in dealerships]
        # Return a list of dealer short name
        context['dealer_list'] = dealerships
        return render(request, 'djangoapp/index.html', context)


def get_dealer_details(request, dealer_id):
    """
    # Create a `get_dealer_details` view to render the reviews of a dealer
    """
    context = {}
    # if request.method == "GET":
    url = api_url + "dealership?id=" + str(dealer_id)
    # Get dealers from the URL
    dealerships = get_dealer_by_id(url, dealerId=dealer_id)
    # Concat all dealer's short name
    # dealer_names = [dealer.short_name for dealer in dealerships]
    # Return a list of dealer short name
    # print(repr(dealerships))
    # print(len(dealerships))
    # print(repr(dealerships[0]))
    # context['dealer_list'] = dealerships[:]
    if len(dealerships) > 0:
        context['dealer'] = dealerships[0]

    url = api_url + "review?id=" + str(dealer_id)
    reviews = get_dealer_reviews_from_cf(url, dealer_id)
    context['review_list'] = reviews
    return render(request, 'djangoapp/dealer_details.html', context)


def add_review(request, dealer_id=None):
    """
    # Submit a review
    """
    print("in add_review: ")
    print(request)
    print(dealer_id)
    response = {}
    print(request.user.is_authenticated)
    print(request.method)

    if request.user.is_authenticated:
        # user is valid
        """
        sample review to post
        {
        "review":
            {
                "id": 1117,
                "name": "Jan-Cees van de Kerk",
                "dealership": 15,
                "review": "Great service! Very helpful.",
                "purchase": true,
                "another": "field",
                "further": "information",
                "purchase_date": "05/16/2020",
                "car_make": "Audi",
                "car_model": "Car",
                "car_year": 2018
            }
        }
        """
        context = {}
        # If it is a GET request, just render the registration page
        if request.method == 'GET':
            url = api_url + "dealership?id=" + str(dealer_id)
            dealerships = get_dealer_by_id(url, dealerId=dealer_id)
            if len(dealerships) > 0:
                context['dealer'] = dealerships[0]
                car_list = CarModel.objects.filter(
                    dealer_id=dealer_id)
                # car_list = cars[:]

                context['car_list'] = car_list
                print(context)
                print(car_list)

            return render(request, 'djangoapp/add_review.html', context)
        # If it is a POST request
        elif request.method == 'POST':
            print("request:", request)
            print("request.path   ", request.path)
            # print("request.GET    ", request.GET)
            print("request.method ", request.method)
            print("request.POST   ", request.POST)
            print("content", request.POST.get('content'))
            print("purchasecheck", request.POST.get('purchasecheck'))
            print("purchasedate", request.POST.get('purchasedate'))

            # print("request.FILES  ", request.FILES)
            # print("request.COOKIES", request.COOKIES)
            # print("request.session", request.session)
            # print("request.META   ", request.META)

            review = {}
            review["time"] = datetime.utcnow().isoformat()
            review["name"] = request.user.first_name + " " + \
                request.user.last_name
            review["dealership"] = dealer_id
            review["review"] = request.POST.get('content')
            # review["text"] = request.POST.get('content')
            review["purchase"] = request.POST.get('purchasecheck') == 'on'
            review["purchase_date"] = request.POST.get('purchasedate')

            car_id = request.POST.get('car')
            if car_id:
                review_car = CarModel.objects.get(
                    dealer_id=dealer_id, id=car_id)
                review["car_make"] = review_car.make.name
                review["car_model"] = review_car.name
                review["car_year"] = review_car.year.year

            # review["review"] = "The service department was helpful"
            # review["purchase"]
            # review["purchase_date"]
            # review["car_make"]
            # review["car_model"]
            # review["car_year"]
            # review["sentiment"]
            url = api_url + "review"

            json_payload = {}
            json_payload["review"] = review
            print("ready to call post_request:", url, json_payload, dealer_id)
            response = post_request(url, json_payload, dealerId=dealer_id)
            # print(response)
            print("back from post request with response", response)
            print("response.content", response.content)
            print("response.headers", response.headers)
            print("response.status_code", response.status_code)
            # dealerId=dealer_id

            return get_dealer_details(request, dealer_id)
    else:
        # user is not vaild - return EnvironmentError
        response['message'] = "User is not authenticated"

    return get_dealer_details(request, dealer_id)


class CarListView(generic.ListView):
    # template_name = 'onlinecourse/course_list.html'
    context_object_name = 'car_list'

    def get_queryset(self):
        cars = CarModel.objects.order_by('name')[:10]
        return cars
