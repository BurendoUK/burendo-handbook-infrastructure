resource "aws_lb" "burendo_handbook_internal_alb" {
  name               = "burendo-handbook-internal-alb"
  internal           = true
  load_balancer_type = "application"
  security_groups    = [aws_security_group.handbook_alb_sg.id]
  subnets            = [aws_subnet.private_subnet_1.id, aws_subnet.private_subnet_2.id]
}

resource "aws_lb_target_group" "burendo_handbook_tg" {
  name     = "burendo-handbook-target-group"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.burendo_handbook_vpc.id
}

resource "aws_lb_listener" "burendo_handbook_listener" {
  load_balancer_arn = aws_lb.burendo_handbook_internal_alb.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.burendo_handbook_tg.arn
  }
}
