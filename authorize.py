"""Authenticate the user with the Sam service."""

from collections.abc import Callable
from flask import request
from functools import wraps
from requests import get, Response
from requests.exceptions import ConnectionError
import werkzeug.exceptions as e


def authorized(sam_root: str) -> Callable[..., any]:
    """Authorization decorator.

    Decorated routes will precheck the request to see if the caller is authorized to perform the operation.
    Taken from example in Sanic documentation: `https://sanic.readthedocs.io/en/latest/sanic/decorators.html`

    Returns:
        Callable of the wrapped function.

    Raises:
        Forbidden: if not authorized
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Check the Terra authorization service SAM for user auth status
            user_is_authorized = _check_sam_authorization(sam_root)
            if user_is_authorized:
                # run the handler method and return the response
                response = f(*args, **kwargs)
                return response
            else:
                raise e.Forbidden
        return decorated_function
    return decorator


def _check_sam_authorization(sam_root: str) -> bool:
    """Query Terra's authorization service SAM to determine user authorization status.

    Returns:
        True if Sam authorizes the user's access; false otherwise.

    Raises:
        ServiceUnavailable: if Sam request fails
        Unauthorized: if no bearer token in request
    """
    sam_url = sam_root + '/register/user/v2/self/info'

    # Well-formed requests must contain an authorization header
    if 'authorization' not in request.headers:
        raise e.Unauthorized('Request requires authorization header supplying Oauth2 bearer token')
    try:
        sam_response = get(sam_url, headers={'authorization': request.headers['authorization']})
        return _process_sam_response(sam_response)
    except ConnectionError:
        raise e.ServiceUnavailable('Service Unavailable. Unable to contact authorization service')


def _process_sam_response(sam_response: Response) -> bool:
    """Check the sam response and respond appropriately.

    Returns:
        True if the user is authorized, otherwise raise a relevant exception with a helpful message.

    Raises:
        Forbidden: if user not enabled in Sam or Sam responds with 403
        Unauthorized: Sam responds with 401
        ServiceUnavailable: Sam responds with 503
        InternalServerError: if Sam response does not contain the expected JSON format or responds with 404 or another non-200 status
    """

    status = sam_response.status_code
    # For an authorized user, we will receive a 200 status code with 'enabled: True' in the response body
    if status == 200:
        if 'enabled' not in sam_response.json():
            raise e.InternalServerError('Internal Server Error. Unable to determine user authorization status')
        elif not sam_response.json()['enabled']:
            raise e.Forbidden('Forbidden. User is registered in Terra, but not activated.')
        else:
            # SAM service returned 200 and the user was enabled. User is authorized.
            return True
    # Intercept non-successful status codes and return a more helpful message
    else:
        if status == 401:
            raise e.Unauthorized('Unauthorized. User is not allowed in Terra or has not signed in.')
        elif status == 403:
            raise e.Forbidden
        elif status == 404:
            raise e.Unauthorized('Unauthorized. User is authenticated to Google but is not a Terra member')
        elif status == 500:
            raise e.InternalServerError('Internal Server Error. Authorization service query failed')
        elif status == 503:
            raise e.ServiceUnavailable('Service Unavailable. Authorization service unable to contact one or more services')
        else:
            raise e.InternalServerError('Internal Server Error. Unknown failure contacting authorization service.')
