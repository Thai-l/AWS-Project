resource "aws_s3_bucket" "bucket_data" {
  bucket = var.bucket_name
  acl    = "private"

  tags = {
    Name   = "MyProjectAn",
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}