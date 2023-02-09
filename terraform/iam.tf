resource "aws_iam_role" "apprunner" {
  name               = "apprunner"
  assume_role_policy = data.aws_iam_policy_document.apprunner_assume_role.json
  tags               = merge(local.tags, { Name = "apprunner" })
}

data "aws_iam_policy_document" "apprunner_assume_role" {
  statement {
    actions = [
      "sts:AssumeRole",
    ]

    principals {
      type = "Service"
      identifiers = [
        "tasks.apprunner.amazonaws.com",
        "build.apprunner.amazonaws.com"
      ]
    }
  }
}

resource "aws_iam_role_policy_attachment" "apprunner_config_attachment" {
  role       = aws_iam_role.apprunner.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSAppRunnerServicePolicyForECRAccess"
}
