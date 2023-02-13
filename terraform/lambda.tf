resource "aws_lambda_function" "test_lambda" {
  filename      = "../lambda/auth.zip"
  function_name = "handbook-auth"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "index.handler"

  source_code_hash = filebase64sha256("../lambda/auth.zip")

  runtime = "nodejs16.x"

  environment {
    variables = {
      USERPOOLID = aws_cognito_user_pool.burendo.id
    }
  }
}
