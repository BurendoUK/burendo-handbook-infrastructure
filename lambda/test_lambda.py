import unittest
from unittest.mock import patch
import json
import jwt
import requests

from lambda_function import lambda_handler

class TestLambdaFunction(unittest.TestCase):

    @patch.dict("os.environ", {"USER_POOL_ID": "test_user_pool_id", "APP_CLIENT_ID": "test_app_client_id", "AWS_DEFAULT_REGION": "test_region"})
    @patch("requests.get")
    def test_valid_token(self, mock_requests_get):
        # Arrange
        payload = {"sub": "test_sub", "token_use": "access"}
        access_token = jwt.encode(payload, "test_secret", algorithm="HS256", headers={"kid": "test_kid"})
        event = {"headers": {"Authorization": f"Bearer {access_token}"}}
        jwks_response = {"keys": [{"kty": "RSA", "kid": "test_kid", "use": "sig", "n": "test_n", "e": "AQAB"}]}
        mock_requests_get.return_value.text = json.dumps(jwks_response)
        with patch("jwt.decode", return_value=payload):
            # Act
            result = lambda_handler(event, None)

        # Assert
        expected_result = {"statusCode": 200, "body": json.dumps({"message": "Access granted"})}
        self.assertEqual(result, expected_result)

    @patch.dict("os.environ", {"USER_POOL_ID": "test_user_pool_id", "APP_CLIENT_ID": "test_app_client_id", "AWS_DEFAULT_REGION": "test_region"})
    @patch("requests.get")
    def test_valid_key(self, mock_requests_get):
        # Arrange
        payload = {"sub": "test_sub", "token_use": "access"}
        invalid_access_token = jwt.encode(payload, "test_secret", algorithm="HS256", headers={"kid": "test_kid"})
        event = {"headers": {"Authorization": f"Bearer {invalid_access_token}"}}
        jwks_response = {"keys": [{"kty": "RSA", "kid": "test_kid_2", "use": "sig", "n": "test_n", "e": "AQAB"}]}
        mock_requests_get.return_value.text = json.dumps(jwks_response)
        result = lambda_handler(event, None)

        # Assert
        expected_result = {"statusCode": 401, "body": json.dumps({"message": "Unable to find appropriate key"})}
        self.assertEqual(result, expected_result)
        
    @patch.dict("os.environ", {"USER_POOL_ID": "test_user_pool_id", "APP_CLIENT_ID": "test_app_client_id", "AWS_DEFAULT_REGION": "test-region"})
    def test_missing_auth_header(self):
        # Arrange
        event = {"headers": {}}
        
        # Act
        result = lambda_handler(event, None)
        
        # Assert
        expected_result = {"statusCode": 401, "body": json.dumps({"message": "Authorization header is missing"})}
        self.assertEqual(result, expected_result)
        
    @patch.dict("os.environ", {"USER_POOL_ID": "test_user_pool_id", "APP_CLIENT_ID": "test_app_client_id", "AWS_DEFAULT_REGION": "test-region"})
    @patch("requests.get")
    def test_invalid_token_use(self, mock_requests_get):
        # Arrange
        payload = {"sub": "test_sub", "token_use": "no_access"}
        access_token = jwt.encode(payload, "test_secret", algorithm="HS256", headers={"kid": "test_kid"})
        event = {"headers": {"Authorization": f"Bearer {access_token}"}}
        jwks_response = {"keys": [{"kty": "RSA", "kid": "test_kid", "use": "sig", "n": "test_n", "e": "AQAB"}]}
        mock_requests_get.return_value.text = json.dumps(jwks_response)
        with patch("jwt.decode", return_value=payload):
            # Act
            result = lambda_handler(event, None)
        
        # Assert
        expected_result = {"statusCode": 401, "body": json.dumps({"message": "Invalid token use"})}
        self.assertEqual(result, expected_result)
        
    @patch.dict("os.environ", {"USER_POOL_ID": "test_user_pool_id", "APP_CLIENT_ID": "test_app_client_id", "AWS_DEFAULT_REGION": "test-region"})
    @patch("requests.get")
    def test_invalid_token_claims(self, mock_requests_get):
        # Arrange
        payload = {"sub": "test_sub", "token_use": "access"} 
        access_token = jwt.encode(payload, "test_secret", algorithm="HS256", headers={"kid": "test_kid"})
        event = {"headers": {"Authorization": f"Bearer {access_token}"}}
        jwks_response = {"keys": [{"kty": "RSA", "kid": "test_kid", "use": "sig", "n": "test_n", "e": "AQAB"}]}
        mock_requests_get.return_value.text = json.dumps(jwks_response)
        jwt_exception = jwt.InvalidTokenError("test_message", payload)
        with patch("jwt.decode", side_effect=jwt_exception):
            # Act
            result = lambda_handler(event, None)
        
        # Assert
        expected_result = {"statusCode": 401, "body": json.dumps({"message": "Invalid token claims"})}
        self.assertEqual(result, expected_result)

    @patch.dict("os.environ", {"USER_POOL_ID": "test_user_pool_id", "APP_CLIENT_ID": "test_app_client_id", "AWS_DEFAULT_REGION": "test_region"})
    @patch("requests.get")
    def test_expired_token(self, mock_requests_get):
        # Arrange
        payload = {"sub": "test_sub", "token_use": "access"}
        access_token = jwt.encode(payload, "test_secret", algorithm="HS256", headers={"kid": "test_kid"})
        event = {"headers": {"Authorization": f"Bearer {access_token}"}}
        jwks_response = {"keys": [{"kty": "RSA", "kid": "test_kid", "use": "sig", "n": "test_n", "e": "AQAB"}]}
        mock_requests_get.return_value.text = json.dumps(jwks_response)
        jwt_exception = jwt.ExpiredSignatureError("test_message", payload)
        with patch("jwt.decode", side_effect=jwt_exception):
            # Act
            result = lambda_handler(event, None)

        # Assert
        expected_result = {"statusCode": 401, "body": json.dumps({"message": "Token has expired"})}
        self.assertEqual(result, expected_result)
