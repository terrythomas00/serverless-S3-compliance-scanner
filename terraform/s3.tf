

resource "aws_s3_bucket" "reports_bucket" {
  bucket = var.bucket_name
  tags = {
    Name = "Reports Bucket"
    Environment = var.environment
  }

}

resource "aws_s3_bucket_server_side_encryption_configuration" "reports_bucket_encryption" {
  bucket = aws_s3_bucket.reports_bucket.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }

}


resource "aws_s3_bucket_versioning" "reports_bucket_versioning" {
  bucket = aws_s3_bucket.reports_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}


resource "aws_s3_bucket_public_access_block" "reports_bucket_public_access" {
  bucket = aws_s3_bucket.reports_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}