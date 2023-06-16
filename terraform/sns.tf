resource "aws_sns_topic" "burendo_handbook_health_check_topic" {
  provider = aws.northvirginia
  name     = "${local.environment}-burendo-handbook-health-check-alarm"
}
