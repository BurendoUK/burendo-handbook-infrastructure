# Burendo Handbook Infrastructure

This repo contains the AWS infrastructure for the Burendo Handbook & the pipeline to pull in the content from the content repos, build docusaurus and deploy.

## The Handbook

### Content
To update the content used to create the handbook, modify in the respective content repo.
[burendo-handbook-public](https://github.com/BurendoUK/burendo-handbook-public)
[burendo-handbook-private](https://github.com/BurendoUK/burendo-handbook-private)

### Architecture
![Handbook architecture](handbook-architecture.png)

### Running locally

Running locally, you will need to bring in the docs from content repos into burendo-handbook/docs.
Then enter `burendo-handbook` folder and run `npm install` && `npm run-script docusaurus start`.

## The Lambda

This AWS Lambda function is a serverless function designed to perform a validation of JSON Web Tokens (JWT) obtained from the Burendo owned Amazon Cognito user pool. The function first checks if the Authorization header is present in the request. If not, it returns a 401 HTTP response with an error message. If the Authorization header is present, the function extracts the access token from the header and retrieves the JSON Web Key Set (JWKS) for the user pool. The function then verifies the signature of the access token using the public key obtained from the JWKS.

The function also checks the claims in the JWT, including the issuer, the audience, the token use, and the expiration time. If any of the checks fail, the function returns a 401 HTTP response with an error message. If all the checks pass, the function returns a 200 HTTP response with a success message.

This function is useful for protecting resources in a serverless architecture using Amazon Cognito for user authentication and authorization. It ensures that only authenticated and authorized users can access protected resources.

### Running "locally (AWS)"

This is an arm64 lambda and the below dependencies are compiled for arm64. Cryptography is compiled for arm64 using the following steps:
1. For VSCode use the `.devcontainer` in the root of the repo to build the lambda: `Shift + CMD + P` and _Choose Reopen in container_
2. From the `lambda/` folder, install cryptography using the following command: `pip3 install --platform manylinux2014_x86_64 --only-binary=:all: --upgrade --target ./package cryptography`
3. Install the below dependencies using the following command: `pip3 install -r requirements.txt --target ./package`
4. Copy the `lambda_function.py` file to the package folder
5. Zip the package folder and upload it to the lambda function

The upload to AWS can be done, either via the console or using Terraform.

You can fire through a manual test in the console using a payload like:

```
{
  "headers": {
    "Authorization": "Bearer eyJraWQiOiJzSFprWjhTN3k5ZVwvODg2MEVXeTFMVU1HaGZWUjlGNlNtYzN5N0o0dnRCdz0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI0NTFhM2NlMi05Y2U0LTRlMzAtOWY2ZS1iNzJiOGEzNDE5NGUiLCJ0b2tlbl91c2UiOiJhY2Nlc3MiLCJzY29wZSI6ImF3cy5jb2duaXRvLnNpZ25pbi51c2VyLmFkbWluIiwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLnVzLWVhc3QtMS5hbWF6b25hd3MuY29tXC91cy1lYXN0LTFfalRoQ3NhUGV6IiwiZXhwIjoxNTA1NjYwMTY2LCJpYXQiOjE1MDU2NTY1NjYsInZlcnNpb24iOjIsImp0aSI6ImI1Yzg5MmIyLTE0NDEtNDQ0OS1hYTRiLTdjYmJmNzg3OTMzNiIsImNsaWVudF9pZCI6IjVoN2VkNGRzdmdzdWdyNWwxZ2RsMzJlcGg3IiwidXNlcm5hbWUiOiJqb2UifQ.V5OqX61MA_hZ-DfxkK-dLTfusIde8X_joqzUmDiAnWnaYk5L2jKgEUNKdXjSnIXL7kgSFx1rXWIGQvF2x4CpCJ7D_u_Ux1aEj-GeM1MyYra8EPgDmt0Eu62UUYRtZ0uUi-EtDWImsZ4cfS4jCeMfBniph4I2GKfjgF2NJoSU9KtfWTaAk7XHv4yML6Q8w_iyBGZDmDYjb7vx6vCXJoc5KnAE87T1MBQByLNhdkhgF8_0YAuSJk9E0Gj6sEbdVoF7dsCO3UkcTjuxZCl3pABorhtbI1HQJk91GiK7Ca4Y_UwV2WqM_eW9qaNKFI6y1MgsRP612uLLhENb8BGc28QCNA"
  },
  "body": {
    "some_key": "some_value"
  }
}
```

### Testing

There are tox unit tests provided for the function in `lambda/test_lambda.py`. To run them, you will need the module tox installed with:  
`pip install tox`  
then go to the root of the module and simply run tox to run all the unit tests.
`tox -p`

These tests are ran whenever a contextual change is made to the Lambda and a PR created.
