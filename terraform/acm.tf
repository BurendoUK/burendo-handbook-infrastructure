resource "aws_acm_certificate" "burendo_handbook" {
  provider          = aws.northvirginia
  domain_name       = local.environment_domain[local.environment]
  validation_method = "DNS"

  tags = merge(local.tags)

  lifecycle {
    create_before_destroy = true
  }
}
