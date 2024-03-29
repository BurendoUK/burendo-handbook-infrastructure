# The Verify Code Lambda

This lambda controls our access process. It logs in using the following process:

1. When clicking Login, AWS Cognito is called and returns a `code`
1. The lambda takes this code and uses it to get an `access token` from Cognito
1. The token is verified but decoding it using AWS and checking the values

Login is controlled via a cookie that allows access for 8 hours. Logging out again will clear this cookie.

When any request comes in for a page, the lambda checks if the cookie is present and valid. If it is, then the user is redirected to the private handbook. If the user is not verified they are redirected to the public handbook. It may be that the page is therefore not present and they would then get a 404.

You can tell if you are logged in or out by the "Login" or "Logout" menu option.

### Running lambda locally (AWS)

This is an arm64 lambda and the below dependencies are compiled for arm64. Cryptography is compiled for arm64 using the following steps:
1. For VSCode use the `.devcontainer` in the root of the repo to build the lambda: `Shift + CMD + P` and _Choose Reopen in container_
1. From the `lambda/verify_build_lambda` folder, install cryptography using the following command: `pip3 install --platform manylinux2014_x86_64 --only-binary=:all: --upgrade --target ./package cryptography`
1. Install the below dependencies using the following command: `pip3 install -r requirements.txt --target ./package`
1. Copy the `lambda_function.py` file to the package folder
1. Zip the package folder and upload it to the lambda function

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
