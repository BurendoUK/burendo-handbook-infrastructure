import json
import boto3

def lambda_handler(event, context):
    print(json.dumps(event))
    return event["Records"][0]["cf"]["request"]
    try:
        request = event["Records"][0]["cf"]["request"]
    except:
        return {
            "statusCode": 401,
            "body": json.dumps({"message": "Authorisation check invoked incorrectly"})
        }

    try:
        origin_name = request["origin"]["s3"]["domainName"]
    except:
        return {
            "statusCode": 401,
            "body": json.dumps({"message": "Origin name missing"})
        }

    try:
        public_s3_bucket_name = request["origin"]["s3"]["customHeaders"]["public_s3_bucket"][0]["value"]
        private_s3_bucket_name = request["origin"]["s3"]["customHeaders"]["private_s3_bucket"][0]["value"]
    except:
        return {
            "statusCode": 401,
            "body": json.dumps({"message": "Custom headers are missing"})
        }

    request["origin"]["s3"]["domainName"] = public_s3_bucket_name

    # Check if the Authorization header is present in the request
    if "Authorization" not in request["headers"]:
        return {
            "statusCode": 401,
            "body": json.dumps({"message": "Authorization header is missing"})
        }
    
    # Extract the access token from the Authorization header
    token = request["headers"]["Authorization"].split()[1]
    
    # Invoke the new Lambda function to decode the JWT payload
    payload = invoke_decode_jwt_lambda(token)
    
    if not payload:
        return {
            "statusCode": 401,
            "body": json.dumps({"message": "Invalid token"})
        }
    
    return request
