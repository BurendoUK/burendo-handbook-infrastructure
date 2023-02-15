// Test that the correct jwksUrl is being constructed using the correct USERPOOLID and region.
// Test that the request to the jwksUrl is successful and returns a 200 status code.
// Test that an error is thrown if the jwksUrl request fails.
// Test that an error is thrown if the jwt token is invalid.
// Test that an error is thrown if the token is not an access token.
// Test that an error is thrown if the token is not from the correct user pool.
// Test that the token is verified successfully if all conditions are met.
// For each test case, you will need to create a mock implementation of the necessary dependencies(e.g.request, jwt) 
// that returns the expected results for the given input parameters.Additionally, you will need to create mock events that simulate the AWS Lambda function input.

// Unit tests for Cognito authentication Lambda function

'use strict';
const jwt = require('jsonwebtoken');
const jwkToPem = require('jwk-to-pem');
const request = require('request-promise');

const { handler } = require('./index');

jest.mock('request-promise');

describe('Cognito authentication Lambda function', () => {
  const USERPOOLID = 'test-pool-id';
  const region = 'eu-west-2';
  const iss = `https://cognito-idp.${region}.amazonaws.com/${USERPOOLID}`;
  const jwksUrl = `https://cognito-idp.${region}.amazonaws.com/${USERPOOLID}/.well-known/jwks.json`;

  const pems = {
    'test-kid': 'mock-pem'
  };

  const mockHeaders = {
    'Authorization': 'Bearer mock-token'
  };

  const mockEvent = {
    Records: [{
      cf: {
        request: {
          headers: mockHeaders
        }
      }
    }]
  };

  const mockToken = jwt.sign({ token_use: 'access', iss: iss }, 'mock-secret', { header: { kid: 'test-kid' } });

  const response401 = { status: '401', statusDescription: 'Unauthorized', body: 'Invalid access token' };
  const response200 = { status: '200', statusDescription: 'OK' };

  const spyJWKSRequest = jest.spyOn(request, 'get').mockImplementation(() => Promise.resolve({ keys: [{ kid: 'test-kid' }] }));

  beforeAll(async () => {
    request.get.mockImplementation(() => Promise.resolve({
      keys: [
        {
          kid: 'test-kid',
          alg: 'RS256',
          use: 'sig',
          n: 'mock-n-value',
          e: 'AQAB',
          x5c: ['mock-x5c-value']
        }
      ]
    }));

    await getJWKS();
  });

  afterEach(() => {
    spyJWKSRequest.mockClear();
  });

  afterAll(() => {
    spyJWKSRequest.mockRestore();
  });

  it('should return 401 if no authorization header found', async () => {
    const result = await handler({ Records: [{ cf: { request: { headers: {} } } }] });
    expect(result).toEqual(response401);
  });

  it('should return 401 if the token is not JWT', async () => {
    const result = await handler({ Records: [{ cf: { request: { headers: { 'Authorization': 'invalid-token' } } } }] });
    expect(result).toEqual(response401);
  });

  it('should return 401 if token is not from the User Pool', async () => {
    const mockTokenWithInvalidIssuer = jwt.sign({ iss: 'https://invalid-issuer.com' }, 'mock-secret');
    const result = await handler({ Records: [{ cf: { request: { headers: { 'Authorization': `Bearer ${ mockTokenWithInvalidIssuer }` } } } }] });
    expect(result).toEqual(response401);
  });

  it('should return 401 if the token is not an access token', async () => {
    const mockTokenWithInvalidUse = jwt.sign({ token_use: 'id' }, 'mock-secret', { header: { kid: 'test-kid' } });
    const result = await handler({ Records: [{ cf: { request: { headers: { 'Authorization': `Bearer ${ mockTokenWithInvalidUse }` } } } }] });
    expect(result).toEqual(response401);
  });

  it('should return 401 if the token is invalid', async () => {
    const result = await handler(mockEvent);
    expect(result).toEqual(response401);
  });

  it('should return 401 if the jwks request fails', async () => {
    spyJWKSRequest.mockImplementationOnce(() => Promise.reject(new Error('Failed to retrieve JWKS')));
    const result = await handler(mockEvent);
    expect(result).toEqual(response401);
  });

  it('should return 401 if the kid is not found in pems', async () => {
    const spyJWKSToPem = jest.spyOn(jwkToPem, 'jwkToPem').mockImplementation(() => 'mock-pem');
    const mockTokenWithInvalidKid = jwt.sign({ token_use: 'access', iss: iss }, 'mock-secret', { header: { kid: 'invalid-kid' } });
    const result = await handler({ Records: [{ cf: { request: { headers: { 'Authorization': `Bearer ${ mockTokenWithInvalidKid }` } } } }] });
    expect(result).toEqual(response401);
    spyJWKSToPem.mockRestore();
  });

  it('should return 200 if the token is valid', async () => {
    const mockDecodedJwt = { header: { kid: 'test-kid' }, payload: { sub: 'test-user-id', iss: iss, token_use: 'access' } };
    const mockValidToken = jwt.sign(mockDecodedJwt.payload, 'mock-pem', { header: mockDecodedJwt.header });
    const result = await handler({ Records: [{ cf: { request: { headers: { 'Authorization': `Bearer ${ mockValidToken }` } } } }] });
    expect(result).toEqual(response200);
  });
})
