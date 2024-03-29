resource "aws_lambda_function" "verify_code_lambda" {
  provider      = aws.northvirginia
  filename      = "../lambda/verify_lambda_build/verify.zip"
  function_name = "verify-code-lambda"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "verify_code_lambda.lambda_handler"
  publish       = true
  timeout       = 30

  source_code_hash = filebase64sha256("../lambda/verify_lambda_build/verify.zip")

  runtime = "python3.8"
}
