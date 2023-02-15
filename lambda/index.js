'use strict';
const jwt = require('jsonwebtoken');
const jwkToPem = require('jwk-to-pem');
const request = require('request-promise');

const USERPOOLID = process.env.USERPOOLID;
const region = 'eu-west-2';
const iss = `https://cognito-idp.${region}.amazonaws.com/${USERPOOLID}`;
const jwksUrl = `https://cognito-idp.${region}.amazonaws.com/${USERPOOLID}/.well-known/jwks.json`;

let pems = {};

async function getJWKS() {
  const options = { json: true, uri: jwksUrl };
  const body = await request(options);
  console.log('JWKS response:', body);
  const keys = body['keys'];
  console.log('JWKS keys:', keys);
  for (let key of keys) {
    pems[key.kid] = jwkToPem(key);
  }
}

getJWKS();

const response401 = {
  status: '401',
  statusDescription: 'Unauthorized'
};

exports.handler = async (event, context) => {
  const cfrequest = event.Records[0].cf.request;
  const headers = cfrequest.headers;

  console.log('getting started');
  console.log(`USERPOOLID=${USERPOOLID}`);
  console.log(`region=${region}`);
  console.log(`pems=${pems}`);

  //Fail if no authorization header found
  if (!headers.authorization) {
    console.log("no auth header");
    return {
      ...response401,
      body: 'No authorization header found',
    };
  }

  //strip out "Bearer " to extract JWT token only
  const jwtToken = headers.authorization[0].value.slice(7);
  console.log(`jwtToken=${jwtToken}`);

  //Fail if the token is not jwt
  const decodedJwt = jwt.decode(jwtToken, { complete: true });
  if (!decodedJwt) {
    console.log("Not a valid JWT token");
    return {
      ...response401,
      body: 'Invalid JWT token',
    };
  }

  //Fail if token is not from your UserPool
  if (decodedJwt.payload.iss !== iss) {
    console.log("invalid issuer");
    return {
      ...response401,
      body: 'Invalid token issuer',
    };
  }

  //Reject the jwt if it's not an 'Access Token'
  if (decodedJwt.payload.token_use !== 'access') {
    console.log("Not an access token");
    return {
      ...response401,
      body: 'Invalid token type',
    };
  }

  //Get the kid from the token and retrieve corresponding PEM
  const kid = decodedJwt.header.kid;
  const pem = pems[kid];
  if (!pem) {
    console.log('Invalid access token');
    return {
      ...response401,
      body: 'Invalid access token',
    };
  }

  //Verify the signature of the JWT token to ensure it's really coming from your User Pool
  try {
    const payload = jwt.verify(jwtToken, pem, { issuer: iss });
    console.log("validated JWT");

    //Valid token. Process the request further

  } catch (e) {
    console.log("Invalid access token");
    return {
      ...response401,
      body: 'Invalid access token',
    };
  }
}
