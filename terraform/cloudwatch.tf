resource "aws_cloudwatch_metric_alarm" "burendo_handbook_health_check_alarm" {
  provider                  = aws
  alarm_name                = "${local.environment}-burendo-handbook-health-check-alarm"
  comparison_operator       = "LessThanThreshold"
  evaluation_periods        = "1"
  metric_name               = "HealthCheckStatus"
  namespace                 = "AWS/Route53"
  period                    = "60"
  statistic                 = "Minimum"
  threshold                 = "1"
  insufficient_data_actions = []
  alarm_actions             = ["${aws_sns_topic.burendo_handbook_health_check_alarm_topic.arn}"]
  alarm_description         = "Send an alarm if burendo handbook is down in ${local.environment}"

  dimensions = {
    HealthCheckId = "${aws_route53_health_check.burendo_handbook_health_check.id}"
  }
}
