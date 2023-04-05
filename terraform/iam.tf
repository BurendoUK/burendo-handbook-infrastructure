data "aws_iam_policy_document" "lambda_assume_role_policy" {
  statement {
    sid    = "AllowAwsToAssumeRole"
    effect = "Allow"

    actions = ["sts:AssumeRole"]

    principals {
      type = "Service"

      identifiers = [
        "edgelambda.amazonaws.com",
        "lambda.amazonaws.com",
      ]
    }
  }
}

resource "aws_iam_role" "iam_for_lambda" {
  name               = "iam_for_lambda"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role_policy.json
}

resource "aws_iam_role_policy_attachment" "lambda_basic_execution_policy_attachment" {
  role       = aws_iam_role.iam_for_lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy" "iam_for_lambda" {
  name   = "iam_for_lambda"
  role   = aws_iam_role.iam_for_lambda.id
  policy = data.aws_iam_policy_document.iam_for_lambda.json
}

data "aws_iam_policy_document" "iam_for_lambda" {
  statement {
    actions = [
      "lambda:InvokeFunction",
    ]

    resources = [
      "arn:aws:lambda:us-east-1:${local.account[local.environment]}:function:${aws_lambda_function.decode_lambda.function_name}",
    ]
  }
}

resource "aws_iam_role_policy" "cloudwatch_for_lambda" {
  name   = "cloudwatch_for_lambda"
  role   = aws_iam_role.iam_for_lambda.id
  policy = data.aws_iam_policy_document.cloudwatch_for_lambda.json
}

data "aws_iam_policy_document" "cloudwatch_for_lambda" {
  statement {
    sid    = "AllowLambdaToCreateLogInAllRegions"
    effect = "Allow"

    actions = [
      "logs:CreateLogGroup",
    ]

    resources = [
      "arn:aws:logs:*:${local.account[local.environment]}:*",
    ]
  }

  statement {
    sid    = "AllowLambdaToLogInAllRegions"
    effect = "Allow"

    actions = [
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]

    resources = [
      "*"
    ]
  }
}
