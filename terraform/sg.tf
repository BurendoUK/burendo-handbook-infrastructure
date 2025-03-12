resource "aws_security_group" "handbook_alb_sg" {
  name   = "burendo-handbook-alb-sg"
  vpc_id = aws_vpc.burendo_handbook_vpc.id

  # Allow incoming HTTP requests from CloudFront
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = data.aws_ip_ranges.cloudfront.cidr_blocks
  }

  # Allow incoming HTTPS requests from CloudFront
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = data.aws_ip_ranges.cloudfront.cidr_blocks
  }

  # Allow ALB to send traffic to backend EC2 instances (no direct SG reference)
  egress {
    from_port   = 3000
    to_port     = 3000
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"] # Allow traffic within the VPC
  }

  tags = {
    Name = "burendo-handbook-alb-sg"
  }
}

resource "aws_security_group" "handbook_instance_sg" {
  name   = "burendo-handbook-instance-sg"
  vpc_id = aws_vpc.burendo_handbook_vpc.id

  # Allow incoming traffic from ALB (no direct SG reference)
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"] # Allow traffic from ALB inside the VPC
  }

  # Allow instances to access AWS services (S3, DynamoDB, etc.)
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "burendo-handbook-instance-sg"
  }
}

resource "aws_security_group" "handbook_ssm_vpc_endpoint_sg" {
  name   = "handbook-ssm-vpc-endpoint-sg"
  vpc_id = aws_vpc.burendo_handbook_vpc.id

  # Allow EC2 instances to talk to SSM VPC Endpoints
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"] # Allow only internal VPC traffic
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "handbook-ssm-vpc-endpoint-sg"
  }
}


data "aws_ip_ranges" "cloudfront" {
  regions  = ["eu-west-2", "us-east-1"]
  services = ["cloudfront"]
}
