# Cache bucket for the billing assistant's rendered account summaries.
# Private (no public access) — but left without encryption, versioning, or access logging.
resource "aws_s3_bucket" "billing_cache" {
  bucket = "support-agent-billing-cache"
}

resource "aws_s3_bucket_public_access_block" "billing_cache" {
  bucket                  = aws_s3_bucket.billing_cache.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
