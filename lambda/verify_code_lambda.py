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
cookie_domain = "handbook.burendo.com"
cookie_path = "/"

LOGIN_SUCCESSFUL_CONTENT = """
<html lang="en">
<head>
    <style>
    body {
        color: white;    
        background-color: black;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 20px;
        text-align: center;
    }
    </style>
    <meta charset="utf-8">
    <title>Burendo Handbook Login Successful</title>
</head>
<body style="text-align:center">
    <p><img src="https://handbook.burendo.com/img/burendo_outline.png" alt="Burendo logo" height="10%">
    <p>You have successfully <strong>logged in</strong> to the Burendo Handbook!</p>
    <p>Click <a href="https://handbook.burendo.com">here</a> to go back to the Home Page.</p>
</body>
</html>
"""

LOGOUT_SUCCESSFUL_CONTENT = """
<html lang="en">
<head>
    <style>
    body {
        color: white;    
        background-color: black;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 20px;
        text-align: center;
    }
    </style>
    <meta charset="utf-8">
    <title>Burendo Handbook Logout Successful</title>
</head>
<body style="text-align:center">
    <p><img src="https://handbook.burendo.com/img/burendo_outline.png" alt="Burendo logo" height="10%">
    <p>You have successfully <strong>logged out</strong> of the Burendo Handbook!</p>
    <p>Click <a href="https://handbook.burendo.com">here</a> to go back to the Home Page.</p>
</body>
</html>
"""

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
        return_object = redirect_unauthorised("Could not parse custom headers")
        print (json.dumps(return_object))
        return return_object

    if is_logout_request(request):
        return_object = logout(request, public_s3_bucket_name);
        print (json.dumps(return_object))
        return return_object
    elif is_login_request(request):
        return_object = login(request, callback_url, client_id, cognito_domain_url, cognito_jwks_url, private_s3_bucket_name)
        print (json.dumps(return_object))
        return return_object

    return_object = get_request(request, public_s3_bucket_name, private_s3_bucket_name)
    print (json.dumps(return_object))
    return return_object

# Check if a login request
def is_logout_request(request):
    query_string = request["querystring"]
    if not query_string:
        return False
    
    try:
        parsed_query_string = parse_qs(query_string)
        print("Query string parsed as to check logout '" + str(parsed_query_string) + "'")
    except:
        return False

    return "logout" in parsed_query_string

# Check if a login request
def is_login_request(request):
    query_string = request["querystring"]
    if not query_string:
        return False
    
    try:
        parsed_query_string = parse_qs(query_string)
        print("Query string parsed as to check code '" + str(parsed_query_string) + "'")
    except:
        return False

    return "code" in parsed_query_string

# Deal with login flow
def login(request, callback_url, client_id, cognito_domain_url, cognito_jwks_url, private_s3_bucket_name):
    print("Logging in")
    query_string = request["querystring"]
    parsed_query_string = parse_qs(query_string)
    code = parsed_query_string["code"][0]
    token = generate_token(code, callback_url, client_id, cognito_domain_url)
    token_dict = token.json()
    print("Token returned as '" + str(token_dict) + "'")
    cookie_value_validated = validate_token(request, token_dict, client_id, cognito_jwks_url, private_s3_bucket_name)
    return redirect_authorised(cookie_value_validated, LOGIN_SUCCESSFUL_CONTENT)

# Deal with logout flow
def logout(request, public_s3_bucket_name):
    print("Logging out")
    expiration = "Thu, 01 Jan 1970 00:00:00 GMT"
    cookie = f"{cookie_key_name}=; Domain={cookie_domain}; expires={expiration}; Path={cookie_path}"
    cookie_value = generate_cookie_header_val(cookie)
    return redirect_authorised(cookie_value, LOGOUT_SUCCESSFUL_CONTENT)

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
    new_request = request
    new_request["origin"]["s3"]["domainName"] = s3_bucket_name
    new_request["headers"]["host"] = [{'key': 'host', 'value': s3_bucket_name}]
    return new_request
    
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
def validate_token(request, token, client_id, cognito_jwks_url, private_s3_bucket_name):
    access_token = token["access_token"]
    public_key_for_decoding = get_public_key(access_token, cognito_jwks_url)
    decoded_id_token = jwt.decode(access_token, key=public_key_for_decoding, algorithms=['RS256'])
    print("Decoded token is '" + str(decoded_id_token) + "'")

    client_id_decoded = decoded_id_token["client_id"]
    if client_id_decoded != client_id:
        return redirect_unauthorised("Invalid id_token.  client_id value does not match expected")

    expiration = (datetime.datetime.now() + datetime.timedelta(hours=6)).strftime("%a, %d %b %Y %H:%M:%S GMT")
    max_age = str(60*60*8) # 8 hours
    value = str(random.randint(0, 1000000000))
    cookie = f"{cookie_key_name}={value}; Domain={cookie_domain}; expires={expiration}; Max-Age={max_age}; Path={cookie_path}; SameSite=None; Secure"
    cookie_value = generate_cookie_header_val(cookie)
    return cookie_value

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
def generate_cookie_header_val(cookie_raw_value):
    cookie = cookies.SimpleCookie()
    cookie.load(cookie_raw_value)
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

# Redirect as logged in or out to set cookies
def redirect_authorised(cookie_value, body_content):
    return {
        'status': '200',
        'statusDescription': 'OK',
        'headers': {
            'set-cookie': [
                {
                    'key': 'Set-Cookie',
                    'value': cookie_value
                }
            ],
            "content-type": [
                {
                    'key': 'Content-Type',
                    'value': 'text/html'
                }
            ]
        },
        'body': body_content
    }
