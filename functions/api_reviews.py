#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter,
# which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
from cloudant.client import Cloudant
from cloudant.error import CloudantException
# from cloudant.result import Result, ResultByKey
import requests


def main(dict):

    print("Current input: ", dict)

    try:
        client = Cloudant.iam(
            account_name=dict["COUCH_USERNAME"],
            api_key=dict["IAM_API_KEY"],
            connect=True,
        )
        # Open the reviews table
        databaseName = "reviews"

        my_database = client[databaseName]

        method = dict.get('__ow_method', 'get')
        dealerId = dict.get('dealerId')
        review_to_add = dict.get('review')
        if review_to_add:
            my_review = my_database.create_document(review_to_add)
            return my_review
        elif method == 'get' and dealerId is None:
            result = {
                'statusCode': 404,
                # 'error': "dealerId does not exist",
                'body': "dealerId does not exist"
            }
            return result
        elif method == 'get':
            selector = {'dealership': {'$eq': int(dict["dealerId"])}}

            fields = ["id", "name", "dealership", "review", "purchase",
                      "purchase_date", "car_make", "car_model", "car_year", ]
            return_by_filter = my_database.get_query_result(
                selector, fields, raw_result=True)
            if len(return_by_filter['docs']) == 0:
                result = {
                    'statusCode': 404,
                    'error': "dealerId does not exist",
                    'body': "dealerId does not exist"
                }
            else:
                result = {
                    'headers': {'Content-Tyope': 'application/json'},
                    'statusCode': 200,
                    'body': {'data': return_by_filter}
                }
            return result
        elif method == 'post':
            print("In POST: ", dict)
            return {
                "body": "in POST",
                "statusCode": 500,
                "message": "in post message"
            }

    except CloudantException as ce:
        print("unable to connect")
        return {
            "error": "Cloudant connection failed with" + ce,
            "statusCode": 500,
            "message": "Cloudant connection failed with" + ce
        }
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {
            "error": "Something went wrong " + err,
            "statusCode": 500,
            "message": "Something went wrong " + err
        }
