import os
import json
import jwt
import requests

USER_POOL_ID = os.environ['USER_POOL_ID']
APP_CLIENT_ID = os.environ['APP_CLIENT_ID']
AWS_DEFAULT_REGION = os.environ['AWS_DEFAULT_REGION']

def decode_jwt(event, context):
    # Get the access token from the Authorization header
    access_token = event['headers']['Authorization'].split()[1]
    # Retrieve the public key for decoding the JWT
    keys_url = f'https://cognito-idp.{AWS_DEFAULT_REGION}.amazonaws.com/{USER_POOL_ID}/.well-known/jwks.json'
    response = requests.get(keys_url)
    jwks = json.loads(response.text)
    key = None
    for k in jwks["keys"]:
        if k['kid'] == jwt.get_unverified_header(access_token)['kid']:
            key = k
            break
    if key is None:
        return {"statusCode": 401, "body": json.dumps({"message": "Missing RSA Key"})}

    # Decode the access token using the public key and verify the signature
    try:
        payload = jwt.decode(access_token, key, algorithms=['RS256'], audience=APP_CLIENT_ID)
        if payload['token_use'] == 'access':
            return {"statusCode": 200, "body": json.dumps({"message": "Access granted"})}
        else:
            return {"statusCode": 401, "body": json.dumps({"message": "Invalid access token"})}
    except jwt.exceptions.InvalidTokenError:
        return {"statusCode": 401, "body": json.dumps({"message": "Invalid access token"})}
