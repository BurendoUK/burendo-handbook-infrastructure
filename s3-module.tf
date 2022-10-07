module "s3_public" {
  source  = "terraform-aws-modules/s3-bucket/aws"
  version = "3.4.0"

  bucket        = "burendo-handbook-public-${local.environment}"
  force_destroy = true
}

module "s3_private" {
  source  = "terraform-aws-modules/s3-bucket/aws"
  version = "3.4.0"

  bucket        = "burendo-handbook-private-${local.environment}"
  force_destroy = true
}

module "log_bucket" {
  source  = "terraform-aws-modules/s3-bucket/aws"
  version = "3.4.0"

  bucket = "burendo-handbook-logs-${local.environment}"
  acl    = null
  grant = [{
    type        = "CanonicalUser"
    permissions = ["FULL_CONTROL"]
    id          = data.aws_canonical_user_id.current.id
    }, {
    type        = "CanonicalUser"
    permissions = ["FULL_CONTROL"]
    id          = "c4c1ede66af53448b93c283ce9448c4ba468c9432aa01d700d3878632f77d2d0"
    # Ref. https://github.com/terraform-providers/terraform-provider-aws/issues/12512
    # Ref. https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/AccessLogs.html
  }]
  force_destroy = true
}

resource "aws_s3_bucket_policy" "public_bucket_policy" {
  bucket = module.s3_public.s3_bucket_id
  policy = data.aws_iam_policy_document.s3_policy.json
}

resource "aws_s3_bucket_policy" "private_bucket_policy" {
  bucket = module.s3_private.s3_bucket_id
  policy = data.aws_iam_policy_document.s3_policy.json
}
