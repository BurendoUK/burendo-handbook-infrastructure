resource "aws_internet_gateway" "burendo_handbook_igw" {
  vpc_id = aws_vpc.burendo_handbook_vpc.id

  tags = {
    Name = "Burendo Handbook IGW"
  }
}
