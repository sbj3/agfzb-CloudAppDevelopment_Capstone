import requests
import json
# import related models here
from .models import CarDealer, DealerReview
# from requests.auth import HTTPBasicAuth

from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

from ibm_watson import NaturalLanguageUnderstandingV1 as NLU

from ibm_watson.natural_language_understanding_v1 import Features
from ibm_watson.natural_language_understanding_v1 import SentimentOptions


def get_request(url, **kwargs):
    """
    # Create a `get_request` to make HTTP GET requests
    # e.g., response = requests.get(
    #       url, params=params,
    #       headers={'Content-Type': 'application/json'},
    #       auth=HTTPBasicAuth('apikey', api_key))
    """
    print("In get_request")

    print(kwargs)
    print("GET from {} ".format(url))

    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(
            url,
            headers={'Content-Type': 'application/json'},
            # auth=HTTPBasicAuth('apikey', api_key),
            params=kwargs)
    except Exception as err:
        # If any error occurs
        print("Network exception occurred " + str(err))
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


def post_request(url, json_payload, **kwargs):
    """
    # Create a `post_request` to make HTTP POST requests
    # e.g., response = requests.post(url, params=kwargs, json=payload)
    """
    results = []

    print("in post_request")
    print("url:", url)
    print("json_payload:", json_payload)
    print("kwargs:", kwargs)
    try:
        response = requests.post(url, params=kwargs, json=json_payload)
        print("back from requests.post with:", response)
        results = response
    except Exception as e:
        print("In post_request, Exception occurred " + str(e))

    return results


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
        dealers = json_result["docs"]
        # print(dealers[0])
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
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

    print("get_dealer_reviews_from_cf")
    results = []
    json_result = get_request(url, dealerId=dealer_id)
    print(json_result)
    if json_result:
        # Get the row list in JSON as reviews
        reviews = json_result["data"]
        review_docs = reviews["docs"]
        # print(reviews[0])
        for review in review_docs:
            print(review)

            review_id = review.get("_id")
            if review_id is not None and review_id[:7] == '_design':
                continue

            review_obj = DealerReview(
                car_make=review.get("car_make"),
                car_model=review.get("car_model"),
                car_year=review.get("car_year"),
                dealership=review["dealership"],
                id=review['id'],
                name=review["name"],
                purchase_date=review.get("purchase_date"),
                purchase=review["purchase"],
                review=review["review"],
                # sentiment=review.get("sentiment"),
                sentiment=analyze_review_sentiments(review)
                )
            results.append(review_obj)

    return results


def analyze_review_sentiments(review):
    """
    # Create an `analyze_review_sentiments` method to call Watson NLU and
    # analyze text
    # def analyze_review_sentiments(text):
    # - Call get_request() with specified arguments
    # - Get the returned sentiment label such as Positive or Negative
    """
    print("In analyze_review_sentiments")
    print(review)

    nlu_api = 'h3DOoDYFxcs' + \
              'oKpssdJDgM2' + \
              'EpXkq0QrWTa' + \
              'xlgETWomK3I'
    nlu_url = 'https://api.us-south.' + \
              'natural-language-understanding.watson.cloud.ibm.com/' + \
              'instances/2861f31e-' + \
              '2af8-4aa2-b27a-' + \
              '82271176a916'
    try:
        authenticator = IAMAuthenticator(nlu_api)
        nl_understanding = NLU(version='2019-07-12',
                               authenticator=authenticator)
        nl_understanding.set_service_url(nlu_url)
        text = review['review']
        response = nl_understanding.analyze(
            text=text,
            features=Features(
                sentiment=SentimentOptions(targets=[text]))).get_result()
        print("after call to NLU analyse")
        print(response)
        # label = json.dumps(response, indent=3)
        label = response['sentiment']['document']['label']
        return(label)
    except Exception as err:
        print("Exception from NaturalLanguageUnderstandingV1 was " + str(err))
        return None
