resource "aws_s3_bucket" "burendo_handbook" {
  bucket = "${local.environment_short_domain[local.environment]}.handbook.burendo.com"
  acl    = "public-read"
  policy = jsonencode({
    Version : "2012-10-17",
    Statement : [
      {
        Sid : "PublicReadGetObject",
        Effect : "Allow",
        Principal : "*",
        Action : "s3:GetObject",
        Resource : "arn:aws:s3:::${local.environment_short_domain[local.environment]}.handbook.burendo.com/*"
      }
    ]
  })

  tags = merge(local.tags, {
    Name = "burendo-handbook"
  })
}

resource "aws_s3_bucket_website_configuration" "burendo_handbook" {
  bucket = aws_s3_bucket.burendo_handbook.id

  index_document {
    suffix = "index.html"
  }

  error_document {
    key = "404.html"
  }
}

output "burendo_handbook_s3" {
  value = aws_s3_bucket.burendo_handbook.id
}
