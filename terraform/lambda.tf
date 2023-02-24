resource "aws_lambda_function" "auth_lambda" {
  provider      = aws.northvirginia
  filename      = "../lambda/auth.zip"
  function_name = "auth-lambda"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "auth_lambda.lambda_handler"
  publish       = true

  source_code_hash = filebase64sha256("../lambda/auth.zip")

  runtime = "python3.8"
}

resource "aws_lambda_function" "decode_lambda" {
  provider      = aws.northvirginia
  filename      = "../lambda/decode.zip"
  function_name = "decode-lambda"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "decode_lambda.lambda_handler"

  source_code_hash = filebase64sha256("../lambda/decode.zip")

  runtime = "python3.8"

  environment {
    variables = {
      USER_POOL_ID  = aws_cognito_user_pool.burendo.id
      APP_CLIENT_ID = aws_cognito_user_pool_client.burendo_client.id
    }
  }
}
