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
  name                = "burendo-handbook-api-env"
  application         = aws_elastic_beanstalk_application.burendo_handbook_api.name
  solution_stack_name = "64bit Amazon Linux 2 running Node.js 18"
  cname_prefix        = "burendo-handbook-api"

  setting {
    namespace = "aws:autoscaling:launchconfiguration"
    name      = "SecurityGroups"
    value     = aws_security_group.handbook_alb_sg.id
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
    namespace = "aws:elasticbeanstalk:environment"
    name      = "EnvironmentType"
    value     = "LoadBalanced" # Use "SingleInstance" for one server
  }

  setting {
    namespace = "aws:autoscaling:launchconfiguration"
    name      = "IamInstanceProfile"
    value     = aws_iam_instance_profile.eb_instance_profile.name
  }

  setting {
    namespace = "aws:elasticbeanstalk:container:nodejs"
    name      = "NodeCommand"
    value     = "npm run start"
  }

  depends_on = [
    aws_security_group.handbook_alb_sg,
    aws_security_group.handbook_instance_sg
  ]
}
