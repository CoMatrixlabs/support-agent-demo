# Bucket for exported billing records — private, encrypted, versioned, access-blocked.
resource "aws_s3_bucket" "billing_exports" {
  bucket = "support-agent-billing-exports"
}

resource "aws_s3_bucket_public_access_block" "billing_exports" {
  bucket                  = aws_s3_bucket.billing_exports.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "billing_exports" {
  bucket = aws_s3_bucket.billing_exports.id
  rule {
    apply_server_side_encryption_by_default { sse_algorithm = "aws:kms" }
  }
}

resource "aws_s3_bucket_versioning" "billing_exports" {
  bucket = aws_s3_bucket.billing_exports.id
  versioning_configuration { status = "Enabled" }
}
