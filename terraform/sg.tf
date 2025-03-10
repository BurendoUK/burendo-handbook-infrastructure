resource "aws_security_group" "handbook_alb_sg" {
  name   = "burendo-handbook-alb-sg"
  vpc_id = aws_vpc.burendo_handbook_vpc.id

  # Allow incoming HTTP requests from CloudFront / S3 (Private AWS Traffic)
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"] # Allow only internal VPC traffic
  }

  # Allow ALB to communicate with EC2 instances
  egress {
    from_port = 80
    to_port   = 80
    protocol  = "tcp"
    self      = true
  }

  tags = {
    Name = "burendo-handbook-alb-sg"
  }
}

resource "aws_security_group" "handbook_instance_sg" {
  name   = "burendo-handbook-instance-sg"
  vpc_id = aws_vpc.burendo_handbook_vpc.id

  # Allow only ALB traffic to reach instances
  ingress {
    from_port       = 80
    to_port         = 80
    protocol        = "tcp"
    security_groups = [aws_security_group.handbook_alb_sg.id]
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
