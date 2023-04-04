resource "aws_s3_bucket" "burendo_handbook" {
  bucket = local.environment_domain[local.environment]

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

resource "aws_s3_bucket_public_access_block" "burendo_handbook_block" {
  bucket = aws_s3_bucket.burendo_handbook.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket" "burendo_handbook_private" {
  bucket = "private.${local.environment_domain[local.environment]}"

  tags = merge(local.tags, {
    Name = "burendo-handbook-private"
  })
}

data "aws_iam_policy_document" "s3_policy_private" {
  statement {
    actions   = ["s3:GetObject"]
    resources = ["${aws_s3_bucket.burendo_handbook_private.arn}/*"]

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

resource "aws_s3_bucket_policy" "burendo_handbook_private" {
  bucket = aws_s3_bucket.burendo_handbook_private.id
  policy = data.aws_iam_policy_document.s3_policy_private.json
}

resource "aws_s3_bucket_public_access_block" "burendo_handbook_private_block" {
  bucket = aws_s3_bucket.burendo_handbook_private.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
