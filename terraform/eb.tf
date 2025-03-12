resource "aws_elastic_beanstalk_application" "burendo_handbook_api" {
  name = "burendo-handbook-api"
}

resource "aws_elastic_beanstalk_application_version" "burendo_handbook_api_version" {
  name        = "burendo-handbook-api-version"
  application = aws_elastic_beanstalk_application.burendo_handbook_api.name
  description = "Initial version of the Burendo Handbook API"
  bucket      = aws_s3_bucket.burendo_handbook_api.bucket
  key         = "burendo-handbook-api.zip"
}

resource "aws_elastic_beanstalk_environment" "burendo_handbook_api_env" {
  name                   = "burendo-handbook-api-env"
  application            = aws_elastic_beanstalk_application.burendo_handbook_api.name
  solution_stack_name    = "64bit Amazon Linux 2023 v6.4.3 running Node.js 22"
  cname_prefix           = "burendo-handbook-api"
  version_label          = aws_elastic_beanstalk_application_version.burendo_handbook_api_version.name
  wait_for_ready_timeout = "10m"

  setting {
    namespace = "aws:autoscaling:launchconfiguration"
    name      = "SecurityGroups"
    value     = aws_security_group.handbook_instance_sg.id
  }

  setting {
    namespace = "aws:ec2:vpc"
    name      = "VPCId"
    value     = aws_vpc.burendo_handbook_vpc.id
  }

  setting {
    namespace = "aws:ec2:vpc"
    name      = "Subnets"
    value     = "${aws_subnet.private_subnet_1.id},${aws_subnet.private_subnet_2.id}"
  }

  setting {
    namespace = "aws:autoscaling:launchconfiguration"
    name      = "InstanceType"
    value     = "t3.medium" # Upgrade from t3.micro to t3.medium or larger
  }

  setting {
    namespace = "aws:elasticbeanstalk:environment"
    name      = "EnvironmentType"
    value     = "SingleInstance" # Use "SingleInstance" for one server
  }

  setting {
    namespace = "aws:autoscaling:launchconfiguration"
    name      = "IamInstanceProfile"
    value     = aws_iam_instance_profile.eb_instance_profile.name
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "SSM_AGENT_ENABLED"
    value     = "true"
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "TINA_PUBLIC_IS_LOCAL"
    value     = "false"
  }

  depends_on = [
    aws_security_group.handbook_alb_sg,
    aws_security_group.handbook_instance_sg
  ]
}
