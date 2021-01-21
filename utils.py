from flask import request
from requests import get
from requests.exceptions import ConnectionError
from functools import wraps
from nbconvert import HTMLExporter
from nbformat.v4 import to_notebook
from werkzeug.exceptions import *
import json

def perform_notebook_conversion(notebook_json):
    # Get the notebook json into a NotebookNode object that nbconvert can use
    nb = to_notebook(notebook_json)

    # set up a default nbconvert HTML exporter and run the conversion
    html_exporter = HTMLExporter()
    (nb_html, resources_dict) = html_exporter.from_notebook_node(nb)
    return nb_html


# Authorization decorator
# Decorated routes will first check the request to see if the caller is authorized to perform the operation
# taken from example in Sanic documentation
# https://sanic.readthedocs.io/en/latest/sanic/decorators.html
def authorized(sam_root):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Check the Terra authorization service SAM for user auth status
            user_is_authorized = __check_sam_authorization(sam_root)
            if user_is_authorized:
                # run the handler method and return the response
                response = f(*args, **kwargs)
                return response
            else:
                raise Forbidden
        return decorated_function
    return decorator


# Query Terra's authorization service SAM to determine user authorization status. Return auth status boolean
def __check_sam_authorization(sam_root):
    sam_url = sam_root + '/register/user/v2/self/info'

    # Well-formed requests must contain an authorization header
    if 'authorization' not in request.headers:
        raise Unauthorized('Request requires authorization header supplying Oauth2 bearer token')
    try:
        sam_response = get(sam_url, headers={'authorization': request.headers['authorization']})
        return __process_sam_response(sam_response)
    except ConnectionError:
        raise ServiceUnavailable('Service Unavailable. Unable to contact authorization service')


# Check the sam response and respond appropriately.
# Return True if the user is authorized, otherwise raise a relevant exception with a helpful message
def __process_sam_response(sam_response):
    # For an authorized user, we will receive a 200 status code with 'enabled: True' in the response body
    status = sam_response.status_code
    if status == 200:
        if 'enabled' not in sam_response.json():
            raise InternalServerError('Internal Server Error. Unable to determine user authorization status')
        elif not sam_response.json()['enabled']:
            raise Forbidden('Forbidden. User is registered in Terra, but not activated.')
        else:
            # SAM service returned 200 and the user was enabled. User is authorized.
            return True
    # Intercept non-successful status codes and return a more helpful message
    else:
        if status == 401:
            raise Unauthorized('Unauthorized. User is not allowed in Terra or has not signed in.')
        elif status == 403:
            raise Forbidden
        elif status == 404:
            raise Unauthorized('Unauthorized. User is authenticated to Google but is not a Terra member')
        elif status == 500:
            raise InternalServerError('Internal Server Error. Authorization service query failed')
        elif status == 503:
            raise ServiceUnavailable('Service Unavailable. Authorization service unable to contact one or more services')
        else:
            raise InternalServerError('Internal Server Error. Unknown failure contacting authorization service.')

def read_json_file(file_name):
    with open(file_name) as json_file:
        data = json.load(json_file)
        return data