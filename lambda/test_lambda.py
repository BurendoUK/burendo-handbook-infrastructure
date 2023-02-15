import json
from unittest.mock import patch, MagicMock

import jwt
import pytest
from botocore.vendored import requests

import lambda_function

# Define some constants for testing
JWT_ALGORITHM = "RS256"
JWT_AUDIENCE = "test-audience"
JWT_ISSUER = "test-issuer"
JWT_EXP_SECONDS = 3600
JWT_NBF_SECONDS = 0
JWT_IAT_SECONDS = 0

def generate_access_token(jwks_url):
    # Generate a JWT access token
    headers = {
        "kid": "test-key-id",
        "alg": JWT_ALGORITHM
    }
    payload = {
        "iss": JWT_ISSUER,
        "aud": JWT_AUDIENCE,
        "exp": JWT_EXP_SECONDS,
        "nbf": JWT_NBF_SECONDS,
        "iat": JWT_IAT_SECONDS,
        "token_use": "access"
    }
    return jwt.encode(payload, headers["kid"], algorithm=JWT_ALGORITHM)

def generate_jwks_response():
    # Generate a mock response for the JWKS endpoint
    jwks = {
        "keys": [
            {
                "alg": JWT_ALGORITHM,
                "kty": "RSA",
                "use": "sig",
                "n": "test-modulus",
                "e": "AQAB",
                "kid": "test-key-id"
            }
        ]
    }
    response = MagicMock()
    response.read.return_value = json.dumps(jwks).encode("utf-8")
    return response

@patch("urllib.request.urlopen")
def test_lambda_handler_valid_token(mock_urlopen):
    # Test that a valid access token is correctly verified
    access_token = generate_access_token("http://example.com/jwks")
    mock_urlopen.return_value = generate_jwks_response()
    event = {"headers": {"Authorization": "Bearer " + access_token.decode()}}
    response = lambda_function.lambda_handler(event, None)
    assert response["statusCode"] == 200
    assert json.loads(response["body"]) == {"message": "Access granted"}

@patch("urllib.request.urlopen")
def test_lambda_handler_missing_auth_header(mock_urlopen):
    # Test that the function returns an error for a missing Authorization header
    event = {"headers": {}}
    response = lambda_function.lambda_handler(event, None)
    assert response["statusCode"] == 401
    assert json.loads(response["body"]) == {"message": "Authorization header is missing"}

@patch("urllib.request.urlopen")
def test_lambda_handler_invalid_token(mock_urlopen):
    # Test that the function returns an error for an invalid access token
    mock_urlopen.return_value = generate_jwks_response()
    event = {"headers": {"Authorization": "Bearer invalid-token"}}
    response = lambda_function.lambda_handler(event, None)
    assert response["statusCode"] == 401
    assert json.loads(response["body"]) == {"message": "Unable to parse token"}

if __name__ == "__main__":
    pytest.main()
