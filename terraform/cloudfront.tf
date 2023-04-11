resource "aws_cloudfront_distribution" "handbook_distribution" {
  depends_on = [
    aws_acm_certificate.burendo_handbook
  ]
  origin {
    domain_name              = aws_s3_bucket.burendo_handbook.bucket_regional_domain_name
    origin_access_control_id = aws_cloudfront_origin_access_control.handbook_distribution_acl.id
    origin_id                = local.s3_origin_id
    dynamic "custom_header" {
      for_each = local.custom_origin_headers
      content {
        name  = custom_header.value.name
        value = custom_header.value.value
      }
    }
  }

  enabled             = true
  is_ipv6_enabled     = true
  default_root_object = "index.html"

  aliases = local.deploy_fqdn[local.environment] == true ? [local.environment_domain[local.environment]] : []

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = local.s3_origin_id
    cache_policy_id  = aws_cloudfront_cache_policy.handbook_distribution_cache_policy.id

    viewer_protocol_policy = "redirect-to-https"

    lambda_function_association {
      event_type   = "origin-request"
      lambda_arn   = aws_lambda_function.verify_code_lambda.qualified_arn
      include_body = true
    }
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
      locations        = []
    }
  }

  price_class = "PriceClass_200"

  tags = merge(local.tags)

  viewer_certificate {
    acm_certificate_arn      = aws_acm_certificate.burendo_handbook.arn
    minimum_protocol_version = "TLSv1.2_2019"
    ssl_support_method       = "sni-only"
  }

  custom_error_response {
    error_code         = 403
    response_code      = 200
    response_page_path = "/index.html"
  }
}

resource "aws_cloudfront_origin_access_control" "handbook_distribution_acl" {
  name                              = "burendo-handbook"
  description                       = "Burendo Handbook Policy"
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}

resource "aws_cloudfront_cache_policy" "handbook_distribution_cache_policy" {
  name        = "handbook-cache-policy"
  default_ttl = 50
  max_ttl     = 100
  min_ttl     = 1
  parameters_in_cache_key_and_forwarded_to_origin {
    cookies_config {
      cookie_behavior = "all"
    }
    headers_config {
      header_behavior = "whitelist"
      headers {
        items = [
          "Authorization",
        ]
      }
    }
    query_strings_config {
      query_string_behavior = "whitelist"
      query_strings {
        items = [
          "code"
        ]
      }
    }
  }
}

output "burendo_handbook_cf_distro" {
  value = aws_cloudfront_distribution.handbook_distribution.domain_name
}
