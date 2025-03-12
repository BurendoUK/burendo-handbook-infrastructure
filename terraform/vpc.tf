resource "aws_vpc" "burendo_handbook_vpc" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_subnet" "private_subnet_1" {
  vpc_id            = aws_vpc.burendo_handbook_vpc.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "eu-west-2a"
}

resource "aws_subnet" "private_subnet_2" {
  vpc_id            = aws_vpc.burendo_handbook_vpc.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "eu-west-2b"
}

resource "aws_subnet" "public_subnet" {
  vpc_id                  = aws_vpc.burendo_handbook_vpc.id
  cidr_block              = "10.0.3.0/24"
  availability_zone       = "eu-west-2a"
  map_public_ip_on_launch = true
}

resource "aws_vpc_endpoint" "handbook_lb_endpoint" {
  vpc_id            = aws_vpc.burendo_handbook_vpc.id
  service_name      = "com.amazonaws.eu-west-2.elasticloadbalancing"
  vpc_endpoint_type = "Interface"
  subnet_ids        = [aws_subnet.private_subnet_1.id, aws_subnet.private_subnet_2.id]
}

resource "aws_vpc_endpoint" "handbook_s3_endpoint" {
  vpc_id          = aws_vpc.burendo_handbook_vpc.id
  service_name    = "com.amazonaws.eu-west-2.s3"
  route_table_ids = [aws_route_table.private_route_table.id]
}

resource "aws_vpc_endpoint" "handbook_ec2_endpoint" {
  vpc_id            = aws_vpc.burendo_handbook_vpc.id
  service_name      = "com.amazonaws.eu-west-2.ec2"
  vpc_endpoint_type = "Interface"
  subnet_ids        = [aws_subnet.private_subnet_1.id, aws_subnet.private_subnet_2.id]
}

resource "aws_vpc_endpoint" "handbook_ssm_endpoint" {
  vpc_id             = aws_vpc.burendo_handbook_vpc.id
  service_name       = "com.amazonaws.eu-west-2.ssm"
  vpc_endpoint_type  = "Interface"
  subnet_ids         = [aws_subnet.private_subnet_1.id, aws_subnet.private_subnet_2.id]
  security_group_ids = [aws_security_group.handbook_ssm_vpc_endpoint_sg.id]
}

resource "aws_vpc_endpoint" "handbook_ssmmessages_endpoint" {
  vpc_id             = aws_vpc.burendo_handbook_vpc.id
  service_name       = "com.amazonaws.eu-west-2.ssmmessages"
  vpc_endpoint_type  = "Interface"
  subnet_ids         = [aws_subnet.private_subnet_1.id, aws_subnet.private_subnet_2.id]
  security_group_ids = [aws_security_group.handbook_ssm_vpc_endpoint_sg.id]
}

resource "aws_vpc_endpoint" "handbook_ec2messages_endpoint" {
  vpc_id             = aws_vpc.burendo_handbook_vpc.id
  service_name       = "com.amazonaws.eu-west-2.ec2messages"
  vpc_endpoint_type  = "Interface"
  subnet_ids         = [aws_subnet.private_subnet_1.id, aws_subnet.private_subnet_2.id]
  security_group_ids = [aws_security_group.handbook_ssm_vpc_endpoint_sg.id]
}

resource "aws_vpc_endpoint" "handbook_logs_endpoint" {
  vpc_id            = aws_vpc.burendo_handbook_vpc.id
  service_name      = "com.amazonaws.eu-west-2.logs"
  vpc_endpoint_type = "Interface"
  subnet_ids        = [aws_subnet.private_subnet_1.id, aws_subnet.private_subnet_2.id]
}

resource "aws_eip" "burendo_handbook_nat_eip" {
  tags = {
    Name = "Burendo Handbook NAT EIP"
  }
}

resource "aws_nat_gateway" "burendo_handbook_nat" {
  allocation_id = aws_eip.burendo_handbook_nat_eip.id
  subnet_id     = aws_subnet.public_subnet.id
}

resource "aws_route_table" "private_route_table" {
  vpc_id = aws_vpc.burendo_handbook_vpc.id
}

resource "aws_route" "private_nat_route" {
  route_table_id         = aws_route_table.private_route_table.id
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id         = aws_nat_gateway.burendo_handbook_nat.id
}

resource "aws_route_table_association" "private_subnet_1_association" {
  subnet_id      = aws_subnet.private_subnet_1.id
  route_table_id = aws_route_table.private_route_table.id
}

resource "aws_route_table_association" "private_subnet_2_association" {
  subnet_id      = aws_subnet.private_subnet_2.id
  route_table_id = aws_route_table.private_route_table.id
}
