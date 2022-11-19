resource "aws_s3_bucket" "burendo_handbook" {
  bucket = local.environment_domain

  tags = merge(local.tags, {
    Name = "burendo-handbook"
  })
}

data "aws_iam_policy_document" "s3_policy" {
  statement {
    actions   = ["s3:GetObject"]
    resources = ["${aws_s3_bucket.burendo_handbook.arn}/*"]

    principals {
      type        = "Service"
      identifiers = ["cloudfront.amazonaws.com"]
    }
    condition {
      test     = "StringEquals"
      variable = "aws:SourceArn"
      values   = ["${aws_cloudfront_distribution.handbook_distribution.arn}"]
    }
  }
}

resource "aws_s3_bucket_policy" "burendo_handbook" {
  bucket = aws_s3_bucket.burendo_handbook.id
  policy = data.aws_iam_policy_document.s3_policy.json
}

output "burendo_handbook_s3" {
  value = aws_s3_bucket.burendo_handbook.id
}
