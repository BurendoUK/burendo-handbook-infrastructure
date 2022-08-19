data "aws_canonical_user_id" "current" {}

data "aws_iam_policy_document" "s3_policy" {
  statement {
    actions = ["s3:GetObject"]
    resources = [
      "${module.s3_public.s3_bucket_arn}/static/*",
      "${module.s3_private.s3_bucket_arn}/static/*"
    ]

    principals {
      type        = "AWS"
      identifiers = module.cloudfront.cloudfront_origin_access_identity_iam_arns
    }
  }
}
