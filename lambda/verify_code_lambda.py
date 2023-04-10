import json
import boto3
import requests
import jwt
import random
import datetime
from http import cookies
from urllib.parse import parse_qs

# If logout path set expired cookie and re-direct to homepage and public origin
# If code then verify, set cookie and private origin
# If cookie header set, the private origin
# Otherwise public origin

cookie_key_name = "_burendo_handbook_session"

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

    if is_logout_request(request):
        return logout();
    elif is_login_request(request):
        return login(request, callback_url, client_id, cognito_domain_url, cognito_jwks_url)

    return get_request(request, public_s3_bucket_name, private_s3_bucket_name)

# Check if a login request
def is_logout_request(request):
    uri = request["uri"]
    return "logout" in uri

# Check if a login request
def is_login_request(request):
    query_string = request["querystring"]
    if not query_string:
        return False
    
    try:
        parsed_query_string = parse_qs(query_string)
        print("Query string parsed as '" + str(parsed_query_string) + "'")
    except:
        return False

    return "code" in parsed_query_string

# Deal with login flow
def login(request, callback_url, client_id, cognito_domain_url, cognito_jwks_url):
    print("Logging in")
    query_string = request["querystring"]
    parsed_query_string = parse_qs(query_string)
    code = parsed_query_string["code"][0]
    token = generate_token(code, callback_url, client_id, cognito_domain_url)
    token_dict = token.json()
    print("Token returned as '" + str(token_dict) + "'")
    return validate_token(token_dict, client_id, cognito_jwks_url)

# Deal with logout flow
def logout():
    print("Logging out")
    cookie_value = generate_cookie_header_val("Thu, 01 Jan 1970 00:00:00 GMT", "")
    return redirect_authorised(cookie_value)

# Deal with standard get request flow
def get_request(request, public_s3_bucket_name, private_s3_bucket_name):
    if is_valid_cookie(request):
        print("Valid cookie, re-directing to private bucket")
        return set_origin_in_request(request, private_s3_bucket_name)
    
    print("No valid cookie present, re-directing to public bucket")
    return set_origin_in_request(request, public_s3_bucket_name)

# Return the session value from the cookie
def is_valid_cookie(request):
    headers = request["headers"]
    if "cookie" not in headers:
        print("Headers does not contain cookie")
        return False
    
    cookie_value = headers["cookie"][0]["value"]

    if not cookie_value:
        print("Cookie is empty")
        return False

    cookie_array = headers["cookie"][0]["value"].split(" ")
    for cookie in cookie_array:
        if cookie_key_name in cookie:
            print("Cookie found with name of '" + cookie_key_name + "'")
            return True

    print("Cookie not found with name of '" + cookie_key_name + "'")
    return False

# Return the session value from the cookie
def set_origin_in_request(request, s3_bucket_name):
    request["origin"]["s3"]["domainName"] = s3_bucket_name
    return request
    
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
        return redirect_unauthorised("Invalid id_token.  client_id value does not match expected")

    expiration = datetime.datetime.now() + datetime.timedelta(hours=6)
    cookie_value = generate_cookie_header_val(expiration.strftime("%a, %d-%b-%Y %H:%M:%S GMT"), random.randint(0, 1000000000))
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
def generate_cookie_header_val(expiry_datetime, cookie_key_value):
    cookie = cookies.SimpleCookie()
    cookie[cookie_key_name] = cookie_key_value
    cookie[cookie_key_name]["expires"] = expiry_datetime
    cookie[cookie_key_name]["path"] = "/"
    cookie[cookie_key_name]['secure'] = True
    cookie[cookie_key_name]['samesite'] = "None"
    cookie[cookie_key_name]['domain'] = "handbook.burendo.com"
    cookie[cookie_key_name]['max-age'] = str(60*60*24)
    raw_cookie_output = cookie.output()
    cookie_value = raw_cookie_output.replace("Set-Cookie: ", "")
    print("Cookie value set to '" + cookie_value + "'")
    return cookie_value

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
