import os
import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen
import time


AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN', 'aafsnd.us.auth0.com')
ALGORITHMS = ['RS256']
API_AUDIENCE = os.environ.get('API_AUDIENCE', 'fsnd_casting_agency')

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header

'''
@TODO implement get_token_auth_header() method
    it should attempt to get the header from the request
        it should raise an AuthError if no header is present
    it should attempt to split bearer and the token
        it should raise an AuthError if the header is malformed
    return the token part of the header
'''
def get_token_auth_header():
    auth_header = request.headers.get("Authorization", None)
    
    if auth_header is None:
        raise AuthError("Missing authorization header", 401)

    bearer_token = auth_header.split(' ')

    if len(bearer_token) != 2:
        raise AuthError("Malformed authorization header", 401)
    elif bearer_token[0].lower() != 'bearer':
        raise AuthError("Authorization header must start with bearer", 401)

    return bearer_token[1]

'''
@TODO implement check_permissions(permission, payload) method
    @INPUTS
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload

    it should raise an AuthError if permissions are not included in the payload
        !!NOTE check your RBAC settings in Auth0
    it should raise an AuthError if the requested permission string is not in the payload permissions array
    return true otherwise
'''
def check_permissions(permission, payload):
    if 'permissions' not in payload:
        abort(400)

    #print(permission)
    #print(payload['permissions'])
    #print()

    if permission not in payload['permissions']:
        raise AuthError('Permission not included in the payload: User Not Authorized', 401)
    
    return True

'''
@TODO implement verify_decode_jwt(token) method
    @INPUTS
        token: a json web token (string)

    it should be an Auth0 token with key id (kid)
    it should verify the token using Auth0 /.well-known/jwks.json
    it should decode the payload from the token
    it should validate the claims
    return the decoded payload

    !!NOTE urlopen has a common certificate error described here: https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
'''
def verify_decode_jwt(token):
    #verify the Auth0  token has kid
    if 'kid' not in jwt.get_unverified_header(token):
        raise AuthError('Not a valid Auth0 token: kid missing', 401)

    # get the jwks
    jwks = json.loads(
        urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json').read()
    )

    # decode the payload
    payload = jwt.decode(
            token, 
            jwks, 
            algorithms=ALGORITHMS,
            audience=API_AUDIENCE,
            issuer=f'https://{AUTH0_DOMAIN}/'
    )

    # validating the claims
    if "iss" in payload and payload["iss"] != f"https://{AUTH0_DOMAIN}/":
        raise AuthError('In valid Issuer', 401)
    if "exp" in payload and payload["exp"] <= time.time():
        raise AuthError('Token expired.', 401)

    return payload

'''
@TODO implement @requires_auth(permission) decorator method
    @INPUTS
        permission: string permission (i.e. 'post:drink')

    it should use the get_token_auth_header method to get the token
    it should use the verify_decode_jwt method to decode the jwt
    it should use the check_permissions method validate claims and check the requested permission
    return the decorator which passes the decoded payload to the decorated method
'''
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator