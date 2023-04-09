import json
import boto3
import requests
import jwt
import random
import datetime
from http import cookies
from urllib.parse import parse_qs

def lambda_handler(event, context):
    print(json.dumps(event))

    try:
        request = event["Records"][0]["cf"]["request"]
        public_s3_bucket_name = request["origin"]["s3"]["customHeaders"]["public_s3_bucket"][0]["value"]
        private_s3_bucket_name = request["origin"]["s3"]["customHeaders"]["private_s3_bucket"][0]["value"]
        callback_url = request["origin"]["s3"]["customHeaders"]["callback_url"][0]["value"]
        client_id = request["origin"]["s3"]["customHeaders"]["client_id"][0]["value"]
        cognito_domain_url = request["origin"]["s3"]["customHeaders"]["cognito_domain_url"][0]["value"]
        cognito_jwks_url = request["origin"]["s3"]["customHeaders"]["cognito_jwks_url"][0]["value"]
    except:
        return redirect_unauthorised("Could not parse custom headers")

    query_string = request["querystring"]
    print("Query string returned as '" + query_string + "'")
    if not query_string:
        return request
    
    try:
        parsed_query_string = parse_qs(query_string)
        print("Query string parsed as '" + str(parsed_query_string) + "'")
    except:
        return redirect_unauthorised("Could not parse query string")

    if "code" not in parsed_query_string:
        print("Code not present in query string, passing request through")
        return request

    code = parsed_query_string["code"][0]
    print("Code parsed as '" + code + "'")

    token = generate_token(code, callback_url, client_id, cognito_domain_url)
    token_dict = token.json()
    print("Token returned as '" + str(token_dict) + "'")
    return validate_token(token_dict, client_id, cognito_jwks_url)
    
# Convert authorisation code to a token
def generate_token(code, callback_url, client_id, cognito_domain_url):
    payload = {
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'redirect_uri': callback_url,
        'code': code
    }

    token_endpoint_url = "{}/oauth2/token".format(cognito_domain_url)
    print("Calling endpoint at '" + token_endpoint_url + "' with payload of '" + str(payload) + "'")
    return requests.post(token_endpoint_url, data=payload)

# Validate the returned token
def validate_token(token, client_id, cognito_jwks_url):
    id_token = token["id_token"]
    access_token = token["access_token"]
    public_key_for_decoding = get_public_key(access_token, cognito_jwks_url)
    decoded_id_token = jwt.decode(access_token, key=public_key_for_decoding, algorithms=['RS256'])
    print("Decoded token is '" + str(decoded_id_token) + "'")

    client_id_decoded = decoded_id_token["client_id"]
    if client_id_decoded != client_id:
        redirect_unauthorised("Invalid id_token.  client_id value does not match expected")

    cookie_value = generate_cookie_header_val()
    print("Cookie value set to '" + cookie_value + "'")
    return redirect_authorised(cookie_value)

# Retrieve the public key used for decoding Cognito JWT
def get_public_key(access_token, cognito_jwks_url):
    jwks_json = requests.get(cognito_jwks_url)
    jwks = jwks_json.json()
    public_keys = {}
    for jwk in jwks['keys']:
        kid = jwk['kid']
        public_keys[kid] = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))
    kid = jwt.get_unverified_header(access_token)['kid']
    return public_keys[kid]

# Generate a cookie header value
def generate_cookie_header_val():
    cookie = cookies.SimpleCookie()
    cookie["session"] = random.randint(0, 1000000000)
    expiration = datetime.datetime.now() + datetime.timedelta(days=1)
    cookie["session"]["expires"] = expiration.strftime("%a, %d-%b-%Y %H:%M:%S GMT")
    cookie["session"]["path"] = "/"
    cookie['session']['secure'] = True
    cookie['session']['samesite'] = "None"
    cookie['session']['domain'] = "handbook.burendo.com"
    cookie['session']['max-age'] = str(60*60*24)
    raw_cookie_output = cookie.output()
    return raw_cookie_output.replace("Set-Cookie: ", "")

# Redirect as unauthorised if not able to validate code and token
def redirect_unauthorised(reason):
    return {
        "status": "401",
        "body": json.dumps({"message": reason})
    }

# If authorised, redirect to homepage with set-cookie
def redirect_authorised(cookie_value):
    return {
        'status': '302',
        'statusDescription': 'User logged in successfully',
        'headers': {
            'location': [
                {
                    'key': 'Location',
                    'value': 'https://handbook.burendo.com/'
                },
            ],
            'set-cookie': [
                {
                    'key': 'Set-Cookie',
                    'value': cookie_value
                }
            ]
        }
    }
