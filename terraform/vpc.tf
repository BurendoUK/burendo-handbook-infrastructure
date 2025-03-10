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

resource "aws_vpc_endpoint" "handbook_vpc_endpoint" {
  vpc_id       = aws_vpc.burendo_handbook_vpc.id
  service_name = "com.amazonaws.eu-west-2.elasticloadbalancing"
  subnet_ids   = [aws_subnet.private_subnet_1.id, aws_subnet.private_subnet_2.id]
}
