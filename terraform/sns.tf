resource "aws_sns_topic" "burendo_handbook_health_check_alarm_topic" {
  provider = aws
  name     = "${local.environment}-burendo-handbook-health-check-alarm"
}
