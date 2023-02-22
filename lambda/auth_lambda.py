import json
import boto3

def lambda_handler(event, context):
    # Check if the Authorization header is present in the request
    if "Authorization" not in event["headers"]:
        return {
            "statusCode": 401,
            "body": json.dumps({"message": "Authorization header is missing"})
        }
    
    # Extract the access token from the Authorization header
    token = event["headers"]["Authorization"].split()[1]
    
    # Invoke the new Lambda function to decode the JWT payload
    payload = invoke_decode_jwt_lambda(token)
    
    if not payload:
        return {
            "statusCode": 401,
            "body": json.dumps({"message": "Invalid token"})
        }
    
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Access granted"})
    }

def invoke_decode_jwt_lambda(token):
    # Set up the client for invoking the Lambda function
    lambda_client = boto3.client('lambda')
    
    # Set the input and payload for the new Lambda function
    input_payload = {
        'token': token
    }
    payload = json.dumps(input_payload)
    
    # Invoke the new Lambda function
    response = lambda_client.invoke(
        FunctionName='decode-lambda',
        Payload=payload
    )
    
    # Parse the response from the new Lambda function
    payload = json.loads(response['Payload'].read().decode())
    
    return payload
