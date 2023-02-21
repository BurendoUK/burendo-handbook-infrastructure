resource "aws_lambda_function" "test_lambda" {
  filename      = "../lambda/lambda.zip"
  function_name = "handbook-auth"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "index.handler"

  source_code_hash = filebase64sha256("../lambda/lambda.zip")

  runtime = "python3.8"

  environment {
    variables = {
      USER_POOL_ID  = aws_cognito_user_pool.burendo.id
      APP_CLIENT_ID = aws_cognito_user_pool_client.burendo_client.id
    }
  }
}
