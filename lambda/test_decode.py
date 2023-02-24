import unittest
from unittest.mock import patch, MagicMock
import json
import jwt

from decode_lambda import decode_jwt

class TestDecodeJWT(unittest.TestCase):

    @patch.dict("os.environ", {"USER_POOL_ID": "test_user_pool_id", "APP_CLIENT_ID": "test_app_client_id", "AWS_DEFAULT_REGION": "test-region"})
    @patch('requests.get')
    def test_valid_token(self, mock_get):
        mock_response = {"keys": [{"kty": "RSA", "kid": "test_kid", "use": "sig", "n": "test_n", "e": "AQAB"}]}
        mock_get.return_value.text = json.dumps(mock_response)
        payload = {"sub": "test_sub", "token_use": "access"}
        access_token = jwt.encode(payload, "test_secret", algorithm="HS256", headers={"kid": "test_kid"})
        event = {"headers": {"Authorization": f"Bearer {access_token}"}}
        print("Event:", event)
        with patch("jwt.decode", return_value=payload):
            # Act
            decoded_payload = decode_jwt(event, None)
        
        expected_payload = {"statusCode": 200, "body": json.dumps({"message": "Access granted"})}
        self.assertDictEqual(decoded_payload, expected_payload)
    
    @patch.dict("os.environ", {"USER_POOL_ID": "test_user_pool_id", "APP_CLIENT_ID": "test_app_client_id", "AWS_DEFAULT_REGION": "test-region"})
    @patch('requests.get')
    def test_invalid_token(self, mock_get):
        mock_response = {"keys": [{"kty": "RSA", "kid": "test_kid", "use": "sig", "n": "test_n", "e": "AQAB"}]}
        mock_get.return_value.text = json.dumps(mock_response)
        payload = {"sub": "test_sub", "token_use": "denied"}
        access_token = jwt.encode(payload, "test_secret", algorithm="HS256", headers={"kid": "test_kid"})
        event = {"headers": {"Authorization": f"Bearer {access_token}"}} 
        with patch("jwt.decode", return_value=payload):
            # Act
            decoded_payload = decode_jwt(event, None)

        expected_result = {"statusCode": 401, "body": json.dumps({"message": "Invalid access token"})}
        self.assertDictEqual(decoded_payload, expected_result)
    
    @patch('requests.get')
    def test_missing_rsa_key(self, mock_get):
        mock_response = {"keys": []}
        mock_get.return_value.text = json.dumps(mock_response)
        # Generate a JWT token
        payload = {"sub": "test_sub", "token_use": "access"}
        access_token = jwt.encode(payload, "test_secret", algorithm="HS256", headers={"kid": "test_kid"})
        # Add the token to the Authorization header in the event
        event = {"headers": {"Authorization": f"Bearer {access_token}"}}
        with patch("jwt.decode", return_value=payload):
            decoded_payload = decode_jwt(event, None)

        expected_result = {"statusCode": 401, "body": json.dumps({"message": "Missing RSA Key"})}
        self.assertDictEqual(decoded_payload, expected_result)
