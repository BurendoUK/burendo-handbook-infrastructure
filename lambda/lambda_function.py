import json
import requests
import jwt
import os

user_pool_id = os.environ["USER_POOL_ID"]
app_client_id = os.environ["APP_CLIENT_ID"]
region = os.environ["AWS_DEFAULT_REGION"]

def lambda_handler(event, context):
    # Check if the Authorization header is present in the request
    if "Authorization" not in event["headers"]:
        return {
            "statusCode": 401,
            "body": json.dumps({"message": "Authorization header is missing"})
        }
    
    # Extract the access token from the Authorization header
    token = event["headers"]["Authorization"].split()[1]
    
    
    # Retrieve the JSON Web Key Set (JWKS) for the user pool to extract the public key corresponding to the "kid" header in the access token
    jwks_url = "https://cognito-idp.{region}.amazonaws.com/{user_pool_id}/.well-known/jwks.json".format(region="region", user_pool_id="user_pool_id")
    response = requests.get(jwks_url)
    jwks = json.loads(response.text)
    
    # Verify the signature of the access token using the public key
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
            break
    if not rsa_key:
        return {
            "statusCode": 401,
            "body": json.dumps({"message": "Unable to find appropriate key"})
        }
    
    try:
        # Check the "iss" and "token_use" claims to ensure that the token is valid and can be used to grant access to protected resources
        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=["RS256"],
            audience="app_client_id",
            issuer="https://cognito-idp.{region}.amazonaws.com/{user_pool_id}".format(region="region", user_pool_id="user_pool_id"),
            options={"verify_exp": False}
        )
        if payload["token_use"] != "access":
            return {
                "statusCode": 401,
                "body": json.dumps({"message": "Invalid token use"})
            }
        else:
            return {
                "statusCode": 200,
                "body": json.dumps({"message": "Access granted"})
            }
    except jwt.ExpiredSignatureError:
        return {
            "statusCode": 401,
            "body": json.dumps({"message": "Token has expired"})
        }
    except jwt.InvalidTokenError:
        return {
            "statusCode": 401,
            "body": json.dumps({"message": "Invalid token claims"})
        }
    except Exception:
        return {
            "statusCode": 401,
            "body": json.dumps({"message": "Unable to parse token"})
        }
