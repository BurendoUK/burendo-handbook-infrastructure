resource "aws_route53_zone" "burendo_handbook" {
  name = local.environment_domain[local.environment]
}

resource "aws_route53_record" "burendo_handbook_ns" {
  zone_id = aws_route53_zone.burendo_handbook.zone_id
  name    = local.environment_domain[local.environment]
  type    = "NS"
  ttl     = "30"
  records = [
    aws_route53_zone.burendo_handbook.name_servers[0],
    aws_route53_zone.burendo_handbook.name_servers[1],
    aws_route53_zone.burendo_handbook.name_servers[2],
    aws_route53_zone.burendo_handbook.name_servers[3],
  ]
  allow_overwrite = true
}

resource "aws_route53_record" "burendo_handbook_acm_validation" {
  for_each = {
    for dvo in aws_acm_certificate.burendo_handbook.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }

  allow_overwrite = true
  name            = each.value.name
  records         = [each.value.record]
  ttl             = 60
  type            = each.value.type
  zone_id         = aws_route53_zone.burendo_handbook.zone_id
}

resource "aws_route53_record" "burendo_handbook" {
  count   = local.deploy_fqdn[local.environment] == true ? 1 : 0
  zone_id = aws_route53_zone.burendo_handbook.zone_id
  name    = local.environment_domain[local.environment]
  type    = "A"

  alias {
    name                   = aws_cloudfront_distribution.handbook_distribution.domain_name
    zone_id                = aws_cloudfront_distribution.handbook_distribution.hosted_zone_id
    evaluate_target_health = false
  }
}

resource "aws_route53_health_check" "burendo_handbook_health_check" {
  provider          = aws.northvirginia
  failure_threshold = "5"
  fqdn              = "handbook.burendo.com"
  port              = 443
  request_interval  = "30"
  resource_path     = "/"
  search_string     = "The Burendo Handbook"
  type              = "HTTPS_STR_MATCH"
}
