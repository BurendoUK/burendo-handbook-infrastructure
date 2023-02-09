resource "aws_apprunner_service" "stackedit" {
  provider     = aws.eire
  service_name = "stackedit"

  source_configuration {
    authentication_configuration {
      access_role_arn = aws_iam_role.apprunner.arn
    }
    image_repository {
      image_configuration {
        port = "8080" #The port that your application listens to in the container                             
      }

      image_identifier      = "${local.account[local.environment]}.dkr.ecr.${local.region}.amazonaws.com/stackedit:latest"
      image_repository_type = "ECR"
    }

  }
}
output "apprunner_service_stackedit" {
  value = aws_apprunner_service.stackedit
}
