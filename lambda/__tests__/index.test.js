// Test that the correct jwksUrl is being constructed using the correct USERPOOLID and region.
// Test that the request to the jwksUrl is successful and returns a 200 status code.
// Test that an error is thrown if the jwksUrl request fails.
// Test that an error is thrown if the jwt token is invalid.
// Test that an error is thrown if the token is not an access token.
// Test that an error is thrown if the token is not from the correct user pool.
// Test that the token is verified successfully if all conditions are met.
// For each test case, you will need to create a mock implementation of the necessary dependencies(e.g.request, jwt) 
// that returns the expected results for the given input parameters.Additionally, you will need to create mock events that simulate the AWS Lambda function input.
