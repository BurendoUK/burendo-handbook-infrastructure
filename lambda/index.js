'use strict';
const jwt = require('jsonwebtoken');
const jwkToPem = require('jwk-to-pem');
const request = require('request');

let USERPOOLID = process.env.USERPOOLID

let jwksUrl = 'https://cognito-idp.' + region + '.amazonaws.com/' + USERPOOLID + '/.well-known/jwks.json';
let options = { json: true };
var region = 'eu-west-2';
var iss = 'https://cognito-idp.' + region + '.amazonaws.com/' + USERPOOLID;
var pems;

pems = {};
request(jwksUrl, options, (error, res, body) => {
  if (error) {
    return console.log(error)
  };
  if (!error && res.statusCode == 200) {
    if (!error && response.statusCode === 200) {
      const keys = body['keys'];
      const jwk = keys.find(k => k.kid === token.header.kid);
      if (!jwk) {
        callback('Invalid token');
      } else {
        const pem = jwkToPem(jwk);
        jwt.verify(token, pem, function (err, decoded) {
          if (err) {
            callback('Invalid token');
          } else {
            // Check if the user belongs to the correct Cognito User Pool
            if (decoded.iss === 'https://cognito-idp.${region}.amazonaws.com/${USERPOOLID}') {
              // Allow the user to access the resource
              callback(null, generatePolicy(decoded.sub, 'Allow', event.methodArn));
            } else {
              callback('Unauthorized');
            }
          }
        });
      }
    } else {
      callback('Unable to retrieve jwks');
    }
  };
});

const response401 = {
  status: '401',
  statusDescription: 'Unauthorized'
};

exports.handler = (event, context, callback) => {
  const cfrequest = event.Records[0].cf.request;
  const headers = cfrequest.headers;
  console.log('getting started');
  console.log('USERPOOLID=' + USERPOOLID);
  console.log('region=' + region);
  console.log('pems=' + pems);

  //Fail if no authorization header found
  if (!headers.authorization) {
    console.log("no auth header");
    callback(null, response401);
    return false;
  }

  //strip out "Bearer " to extract JWT token only
  var jwtToken = headers.authorization[0].value.slice(7);
  console.log('jwtToken=' + jwtToken);

  //Fail if the token is not jwt
  var decodedJwt = jwt.decode(jwtToken, { complete: true });
  if (!decodedJwt) {
    console.log("Not a valid JWT token");
    callback(null, response401);
    return false;
  }

  //Fail if token is not from your UserPool
  if (decodedJwt.payload.iss != iss) {
    console.log("invalid issuer");
    callback(null, response401);
    return false;
  }

  //Reject the jwt if it's not an 'Access Token'
  if (decodedJwt.payload.token_use != 'access') {
    console.log("Not an access token");
    callback(null, response401);
    return false;
  }

  //Get the kid from the token and retrieve corresponding PEM
  var kid = decodedJwt.header.kid;
  var pem = pems[kid];
  if (!pem) {
    console.log('Invalid access token');
    callback(null, response401);
    return false;
  }

  //Verify the signature of the JWT token to ensure it's really coming from your User Pool
  jwt.verify(jwtToken, pem, { issuer: iss }, function (err, payload) {
    if (err) {
      console.log('Token failed verification');
      callback(null, response401);
      return false;
    } else {
      //Valid token. 
      console.log('Successful verification');
      //remove authorization header
      delete cfrequest.headers.authorization;
      //CloudFront can proceed to fetch the content from origin
      callback(null, cfrequest);
      return true;
    }
  });
};
