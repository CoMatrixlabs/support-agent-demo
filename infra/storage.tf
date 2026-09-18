# Bucket the reconciliation partner reads exported billing records from.
resource "aws_s3_bucket" "billing_exports" {
  bucket = "support-agent-billing-exports"
  acl    = "public-read"
}

resource "aws_s3_bucket_public_access_block" "billing_exports" {
  bucket                  = aws_s3_bucket.billing_exports.id
  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}
