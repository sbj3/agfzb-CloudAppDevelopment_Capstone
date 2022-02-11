import requests
import json
# import related models here
from .models import CarDealer, DealerReview
# from requests.auth import HTTPBasicAuth


def get_request(url, **kwargs):
    """
    # Create a `get_request` to make HTTP GET requests
    # e.g., response = requests.get(
    #       url, params=params,
    #       headers={'Content-Type': 'application/json'},
    #       auth=HTTPBasicAuth('apikey', api_key))
    """
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(
            url,
            headers={'Content-Type': 'application/json'},
            params=kwargs)
    except Exception as err:
        # If any error occurs
        print("Network exception occurred " + str(err))
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


def get_dealers_from_cf(url, **kwargs):
    """
    # Create a get_dealers_from_cf method to get dealers from a cloud function
    # def get_dealers_from_cf(url, **kwargs):
    # - Call get_request() with specified arguments
    # - Parse JSON results into a CarDealer object list
    """
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["rows"]
        # print(dealers[0])
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            dealer_id = dealer_doc.get("_id")
            if dealer_id[:7] == '_design':
                continue
            # print(dealer_doc)
            # Create a CarDealer object with values in `doc` object

            dealer_obj = CarDealer(
                address=dealer_doc["address"], city=dealer_doc["city"],
                full_name=dealer_doc["full_name"], id=dealer_doc["id"],
                lat=dealer_doc["lat"], long=dealer_doc["long"],
                short_name=dealer_doc["short_name"],
                st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results


def get_dealer_by_id(url, dealerId, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, dealerId=dealerId)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["rows"]
        # print(dealers[0])
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            dealer_id = dealer_doc.get("_id")
            if dealer_id[:7] == '_design':
                continue
            # print(dealer_doc)
            # Create a CarDealer object with values in `doc` object

            dealer_obj = CarDealer(
                address=dealer_doc["address"], city=dealer_doc["city"],
                full_name=dealer_doc["full_name"], id=dealer_doc["id"],
                lat=dealer_doc["lat"], long=dealer_doc["long"],
                short_name=dealer_doc["short_name"],
                st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results


def get_dealers_by_state(url, state, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, state=state)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["rows"]
        # print(dealers[0])
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            dealer_id = dealer_doc.get("_id")
            if dealer_id[:7] == '_design':
                continue
            # print(dealer_doc)
            # Create a CarDealer object with values in `doc` object

            dealer_obj = CarDealer(
                address=dealer_doc["address"], city=dealer_doc["city"],
                full_name=dealer_doc["full_name"], id=dealer_doc["id"],
                lat=dealer_doc["lat"], long=dealer_doc["long"],
                short_name=dealer_doc["short_name"],
                st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results


def get_dealer_reviews_from_cf(url, dealer_id, **kwargs):
    """
    # Create a get_dealer_reviews_from_cf method to get reviews by dealer id
    # from a cloud function
    # def get_dealer_by_id_from_cf(url, dealerId):
    # - Call get_request() with specified arguments
    # - Parse JSON results into a DealerView object list

            {
                'car_make': 'Audi',
                'car_model': 'Car',
                'car_year': 2021,
                'dealership': 15,
                'id': 1114,
                'name': 'Upkar Lidder',
                'purchase': False,
                'purchase_date': '02/16/2021',
                'review': 'Great service!'
            }
    """

    results = []
    json_result = get_request(url, dealerId=dealer_id)
    print(json_result)
    if json_result:
        # Get the row list in JSON as reviews
        reviews = json_result["data"]
        review_docs = reviews["docs"]
        # print(reviews[0])
        for review in review_docs:
            review_id = review.get("_id")
            if review_id is not None and review_id[:7] == '_design':
                continue

            review_obj = DealerReview(
                car_make=review["car_make"],
                car_model=review["car_model"],
                car_year=review["car_year"],
                dealership=review["dealership"],
                id=review['id'],
                name=review["name"],
                purchase_date=review["purchase_date"],
                purchase=review["purchase"],
                review=review["review"],
                sentiment=review.get("sentiment"),
                )
            results.append(review_obj)

    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and
# analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
