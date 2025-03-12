resource "aws_lb" "burendo_handbook_internal_alb" {
  name               = "burendo-handbook-internal-alb"
  internal           = true
  load_balancer_type = "application"
  security_groups    = [aws_security_group.handbook_alb_sg.id]
  subnets            = [aws_subnet.private_subnet_1.id, aws_subnet.private_subnet_2.id]
  depends_on         = [aws_internet_gateway.burendo_handbook_igw]
}

resource "aws_lb_target_group" "burendo_handbook_http_tg" {
  name     = "burendo-handbook-http-tg"
  port     = 80 # Change from 80 to 3000
  protocol = "HTTP"
  vpc_id   = aws_vpc.burendo_handbook_vpc.id
}

resource "aws_lb_listener" "burendo_handbook_http_listener" {
  load_balancer_arn = aws_lb.burendo_handbook_internal_alb.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.burendo_handbook_http_tg.arn
  }
}

# resource "aws_lb_target_group" "burendo_handbook_https_tg" {
#   name     = "burendo-handbook-https-tg"
#   port     = 443 # Change from 80 to 3000
#   protocol = "HTTPS"
#   vpc_id   = aws_vpc.burendo_handbook_vpc.id
# }

# resource "aws_lb_listener" "burendo_handbook_https_listener" {
#   load_balancer_arn = aws_lb.burendo_handbook_internal_alb.arn
#   port              = 443
#   protocol          = "HTTPS"
#   ssl_policy        = "ELBSecurityPolicy-2016-08"
#   certificate_arn   = aws_acm_certificate.burendo_handbook.arn

#   default_action {
#     type             = "forward"
#     target_group_arn = aws_lb_target_group.burendo_handbook_https_tg.arn
#   }
# }
