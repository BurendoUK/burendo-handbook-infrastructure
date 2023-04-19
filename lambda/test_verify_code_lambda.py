import unittest
from unittest.mock import patch, call
import json
import verify_code_lambda

def get_valid_event():
    return {
        "Records": [
            {
                "cf": {
                    "request": {
                        "origin": {
                            "s3": {
                                "customHeaders": {
                                    "public_s3_bucket": [
                                        {
                                            "key": "public_s3_bucket",
                                            "value": "test_public_s3_bucket"
                                        },
                                    ],
                                    "private_s3_bucket": [
                                        {
                                            "key": "private_s3_bucket",
                                            "value": "test_private_s3_bucket"
                                        },
                                    ],
                                    "callback_url": [
                                        {
                                            "key": "callback_url",
                                            "value": "test_callback_url"
                                        },
                                    ],
                                    "client_id": [
                                        {
                                            "key": "client_id",
                                            "value": "test_client_id"
                                        },
                                    ],
                                    "cognito_domain_url": [
                                        {
                                            "key": "cognito_domain_url",
                                            "value": "test_cognito_domain_url"
                                        },
                                    ],
                                    "cognito_jwks_url": [
                                        {
                                            "key": "cognito_jwks_url",
                                            "value": "test_cognito_jwks_url"
                                        },
                                    ]
                                }
                            }
                        }
                    }
                }
            }
        ]
    }

class TestLambdaFunction(unittest.TestCase):

    def test_handler_missing_args(self):
        event = get_valid_event()
        event["Records"][0]["cf"]["request"]["origin"]["s3"]["customHeaders"].pop("public_s3_bucket")
        expected_result = {"test_result": "result"}
        with patch("verify_code_lambda.redirect_unauthorised", return_value=expected_result) as mock_redirect_unauthorised:
            result = verify_code_lambda.lambda_handler(event, None)

        mock_redirect_unauthorised.assert_called_once_with("Could not parse custom headers")
        self.assertEqual(result, expected_result)

    def test_handler_logout_request(self):
        event = get_valid_event()
        expected_result = {"test_result": "result"}
        with patch("verify_code_lambda.is_logout_request", return_value=True) as mock_is_logout_request:
            with patch("verify_code_lambda.logout", return_value=expected_result) as mock_logout:
                with patch("verify_code_lambda.is_login_request", return_value=False) as mock_is_login_request:
                    with patch("verify_code_lambda.login", return_value=None) as mock_login:
                        with patch("verify_code_lambda.get_request", return_value=expected_result) as mock_get_request:
                            result = verify_code_lambda.lambda_handler(event, None)

        request = event["Records"][0]["cf"]["request"]

        mock_is_logout_request.assert_called_once_with(request)
        mock_logout.assert_called_once_with(request, "test_public_s3_bucket")
        mock_is_login_request.assert_not_called()
        mock_login.assert_not_called()
        mock_get_request.assert_not_called()
        self.assertEqual(result, expected_result)

    def test_handler_login_request(self):
        event = get_valid_event()
        expected_result = {"test_result": "result"}
        with patch("verify_code_lambda.is_logout_request", return_value=False) as mock_is_logout_request:
            with patch("verify_code_lambda.logout", return_value=None) as mock_logout:
                with patch("verify_code_lambda.is_login_request", return_value=True) as mock_is_login_request:
                    with patch("verify_code_lambda.login", return_value=expected_result) as mock_login:
                        with patch("verify_code_lambda.get_request", return_value=expected_result) as mock_get_request:
                            result = verify_code_lambda.lambda_handler(event, None)

        request = event["Records"][0]["cf"]["request"]

        mock_is_logout_request.assert_called_once_with(request)
        mock_is_login_request.assert_called_once_with(request)
        mock_login.assert_called_once_with(request, "test_callback_url", "test_client_id", "test_cognito_domain_url", "test_cognito_jwks_url")
        mock_logout.assert_not_called()
        mock_get_request.assert_not_called()
        self.assertEqual(result, expected_result)

    def test_handler_get_request(self):
        event = get_valid_event()
        expected_result = {"test_result": "result"}
        with patch("verify_code_lambda.is_logout_request", return_value=False) as mock_is_logout_request:
            with patch("verify_code_lambda.logout", return_value=None) as mock_logout:
                with patch("verify_code_lambda.is_login_request", return_value=False) as mock_is_login_request:
                    with patch("verify_code_lambda.login", return_value=None) as mock_login:
                        with patch("verify_code_lambda.get_request", return_value=expected_result) as mock_get_request:
                            result = verify_code_lambda.lambda_handler(event, None)

        request = event["Records"][0]["cf"]["request"]

        mock_is_logout_request.assert_called_once_with(request)
        mock_is_login_request.assert_called_once_with(request)
        mock_get_request.assert_called_once_with(request, "test_public_s3_bucket", "test_private_s3_bucket")
        mock_login.assert_not_called()
        mock_logout.assert_not_called()
        self.assertEqual(result, expected_result)
        
    def test_get_request_valid_cookie(self):
        request = {}
        expected_result = "test_result"
        with patch("verify_code_lambda.is_valid_cookie", return_value=True):
            with patch("verify_code_lambda.set_origin_in_request", return_value=expected_result) as mock_set_origin_in_request:
                result = verify_code_lambda.get_request(request, "test_public_s3_buekct", "test_private_s3_bucket")
        
        mock_set_origin_in_request.assert_called_once_with(request, "test_private_s3_bucket")
        self.assertEqual(result, expected_result)
        
    def test_get_request_invalid_cookie(self):
        request = {}
        expected_result = "test_result"
        with patch("verify_code_lambda.is_valid_cookie", return_value=False):
            with patch("verify_code_lambda.set_origin_in_request", return_value=expected_result) as mock_set_origin_in_request:
                result = verify_code_lambda.get_request(request, "test_public_s3_buekct", "test_private_s3_bucket")
        
        mock_set_origin_in_request.assert_called_once_with(request, "test_public_s3_buekct")
        self.assertEqual(result, expected_result)
    
    def test_is_valid_cookie_is_valid_with_single_cookie(self):
        request = {
            "headers": {
                "cookie":[{'key': 'host', 'value':  "_burendo_handbook_session=1"}]
            }
        }
        result = verify_code_lambda.is_valid_cookie(request)
        expected_result = True
        self.assertEqual(result, expected_result)
    
    def test_is_valid_cookie_is_valid_with_multiple_cookie(self):
        request = {
            "headers": {
                "cookie":[{'key': 'host', 'value':  "test_cookie=2 _burendo_handbook_session=1"}]
            }
        }
        result = verify_code_lambda.is_valid_cookie(request)
        expected_result = True
        self.assertEqual(result, expected_result)
    
    def test_is_valid_cookie_has_no_cookie_header(self):
        request = {
            "headers": {
                "not_a_cookie":[{'key': 'host', 'value':  "_burendo_handbook_session=1"}]
            }
        }
        result = verify_code_lambda.is_valid_cookie(request)
        expected_result = False
        self.assertEqual(result, expected_result)
    
    def test_is_valid_cookie_has_empty_cookie(self):
        request = {
            "headers": {
                "cookie":[{'key': 'host', 'value':  ""}]
            }
        }
        result = verify_code_lambda.is_valid_cookie(request)
        expected_result = False
        self.assertEqual(result, expected_result)
    
    def test_is_valid_cookie_has_no_burendo_cookie(self):
        request = {
            "headers": {
                "cookie":[{'key': 'host', 'value':  "test_cookie=1"}]
            }
        }
        result = verify_code_lambda.is_valid_cookie(request)
        expected_result = False
        self.assertEqual(result, expected_result)
    
    def test_set_origin_in_request(self):
        request = {
            "origin": {
                "s3": {}
            },
            "headers": {}
        }
        result = verify_code_lambda.set_origin_in_request(request, "test_s3_bucket")
        expected_result = {
            "origin": {
                "s3": {"domainName": "test_s3_bucket"}
            },
            "headers": {
                "host":[{'key': 'host', 'value':  "test_s3_bucket"}]
            }
        }
        self.assertDictEqual(result, expected_result)
    
    def test_is_login_request(self):
        request = {"querystring":"code=test_value"}
        with patch("verify_code_lambda.check_value_in_query_string", return_value=True) as mock_check_value_in_query_string:
            result = verify_code_lambda.is_login_request(request)
        expected_result = True
        mock_check_value_in_query_string.assert_called_once_with(request, "code")
        self.assertEqual(result, expected_result)
    
    def test_is_logout_request(self):
        request = {"querystring":"code=test_value"}
        with patch("verify_code_lambda.check_value_in_query_string", return_value=True) as mock_check_value_in_query_string:
            result = verify_code_lambda.is_logout_request(request)
        expected_result = True
        mock_check_value_in_query_string.assert_called_once_with(request, "logout")
        self.assertEqual(result, expected_result)
    
    def test_check_value_in_query_string_is_valid(self):
        result = verify_code_lambda.check_value_in_query_string({"querystring":"test=true"}, "test")
        expected_result = True
        self.assertEqual(result, expected_result)
    
    def test_check_value_in_query_string_is_not_dependant_on_field_value(self):
        result = verify_code_lambda.check_value_in_query_string({"querystring":"test=test"}, "test")
        expected_result = True
        self.assertEqual(result, expected_result)
    
    def test_check_value_in_query_string_is_invalid_query_string(self):
        result = verify_code_lambda.check_value_in_query_string({"querystring":"not_a_query_string"}, "test")
        expected_result = False
        self.assertEqual(result, expected_result)
    
    def test_check_value_in_query_string_has_no_query_string(self):
        result = verify_code_lambda.check_value_in_query_string({"not_querystring":"test=test_value"}, "test")
        expected_result = False
        self.assertEqual(result, expected_result)
    
    def test_check_value_in_query_string_has_no_field(self):
        result = verify_code_lambda.check_value_in_query_string({"querystring":"not_a_test=test_value"}, "test")
        expected_result = False
        self.assertEqual(result, expected_result)
        
    def test_generate_token(self):
        payload = {
            'grant_type': 'authorization_code',
            'client_id': "test_client_id",
            'redirect_uri': "test_url",
            'code': "test_code"
        }
        token_endpoint_url = "test_cognito_url/oauth2/token"
        expected_result = "test_cookie"

        with patch("requests.post", return_value=expected_result) as mock_post_token_request:
            result = verify_code_lambda.generate_token("test_code", "test_url", "test_client_id", "test_cognito_url")
        
        mock_post_token_request.assert_called_once_with(token_endpoint_url, data=payload)
        self.assertEqual(result, expected_result)
        
    def test_validate_token_valid_token(self):
        token = {"access_token": "test_access_token"}
        public_key_for_decoding = "test_public_key"
        decoded_id_token = {"client_id": "test_client_id"}
        expiration_date = "test_expiration_date"
        cookie_value = "test_cookie_value"
        cookie = "_burendo_handbook_session=test_cookie_value; Domain=handbook.burendo.com; expires=test_expiration_date; Max-Age=28800; Path=/; SameSite=None; Secure"
        expected_result = "test_cookie"

        with patch("verify_code_lambda.get_public_key", return_value=public_key_for_decoding) as mock_get_public_key:
            with patch("jwt.decode", return_value=decoded_id_token) as mock_decode_id:
                with patch("verify_code_lambda.get_cookie_expiration_date", return_value=expiration_date) as mock_get_cookie_expiration_date:
                    with patch("verify_code_lambda.get_cookie_value", return_value=cookie_value) as mock_get_cookie_value:
                        with patch("verify_code_lambda.generate_cookie_header_val", return_value=expected_result) as mock_generate_cookie_header_val:
                            result = verify_code_lambda.validate_token(token, "test_client_id", "test_url")
        
        mock_get_public_key.assert_called_once_with("test_access_token", "test_url")
        mock_decode_id.assert_called_once_with("test_access_token", key="test_public_key", algorithms=['RS256'])
        mock_get_cookie_expiration_date.assert_called_once()
        mock_get_cookie_value.assert_called_once()
        mock_generate_cookie_header_val.assert_called_once_with(cookie)
        self.assertEqual(result, expected_result)
        
    def test_validate_token_invalid_token(self):
        token = {"access_token": "test_access_token"}
        public_key_for_decoding = "test_public_key"
        decoded_id_token = {"client_id": "test_client_id"}
        expiration_date = "test_expiration_date"
        cookie_value = "test_cookie_value"
        cookie = "_burendo_handbook_session=test_cookie_value; Domain=handbook.burendo.com; expires=test_expiration_date; Max-Age=28800; Path=/; SameSite=None; Secure"
        expected_result = "test_return"

        with patch("verify_code_lambda.get_public_key", return_value=public_key_for_decoding) as mock_get_public_key:
            with patch("jwt.decode", return_value=decoded_id_token) as mock_decode_id:
                with patch("verify_code_lambda.redirect_unauthorised", return_value=expected_result) as mock_redirect_unauthorised:
                    result = verify_code_lambda.validate_token(token, "not_a_test_client_id", "test_url")
        
        mock_get_public_key.assert_called_once_with("test_access_token", "test_url")
        mock_decode_id.assert_called_once_with("test_access_token", key="test_public_key", algorithms=['RS256'])
        mock_redirect_unauthorised.assert_called_once_with("Invalid id_token.  client_id value does not match expected")

        self.assertEqual(result, expected_result)
        
    def test_get_public_key(self):
        key_1 = {
            "kid": "test_kid",
            "alg": "RS256",
            "kty": "RSA",
            "e": "AQAB",
            "n": "1234567890",
            "use": "sig"
        }
        key_2 = {
            "kid": "test_kid_2",
            "alg": "RS256",
            "kty": "RSA",
            "e": "AQAB",
            "n": "987654321",
            "use": "sig"
        }
        jwks_json = {
            "keys": [key_1, key_2]
        }
        expected_result = "test_public_key"
        kid_return_value = {"kid": "test_kid"}

        with patch("verify_code_lambda.get_jwks_request", return_value=jwks_json) as mock_get_jwks_request:
            with patch("verify_code_lambda.get_jwk_public_key", return_value=expected_result) as mock_get_jwk_public_key:
                with patch("jwt.get_unverified_header", return_value=kid_return_value) as mock_get_unverified_header:
                    result = verify_code_lambda.get_public_key("test_access_token", "test_cognito_url")
        
        mock_get_jwk_public_key_calls = [call(key_1), call(key_2)]

        mock_get_jwks_request.assert_called_once_with("test_cognito_url")
        mock_get_jwk_public_key.assert_has_calls(mock_get_jwk_public_key_calls, any_order=True)
        mock_get_unverified_header.assert_called_once_with("test_access_token")

        self.assertEqual(result, expected_result)
    
    def test_generate_cookie_header_val(self):
        result = verify_code_lambda.generate_cookie_header_val("test_cookie=1; Domain=test.com; expires=Thu, 01 Jan 1970 00:00:00 GMT; Max-Age=1; Path=/; SameSite=None; Secure")
        expected_result = "test_cookie=1; Domain=test.com; expires=Thu, 01 Jan 1970 00:00:00 GMT; Max-Age=1; Path=/; SameSite=None; Secure"
        self.assertEqual(result, expected_result)
    
    def test_redirect_unauthorised(self):
        result = verify_code_lambda.redirect_unauthorised("test_reason")
        expected_result = {"status": "401","body": json.dumps({"message": "test_reason"})}
        self.assertDictEqual(result, expected_result)
    
    def test_redirect_authorised(self):
        result = verify_code_lambda.redirect_authorised("test_cookie", {"test_content": "test_content_value"})
        expected_result = {
            'status': '200',
            'statusDescription': 'OK',
            'headers': {
                'set-cookie': [
                    {
                        'key': 'Set-Cookie',
                        'value': 'test_cookie'
                    }
                ],
                "content-type": [
                    {
                        'key': 'Content-Type',
                        'value': 'text/html'
                    }
                ]
            },
            'body': {"test_content": "test_content_value"}
        }
        self.assertDictEqual(result, expected_result)
