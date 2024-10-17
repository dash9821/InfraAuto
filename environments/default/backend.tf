#Create an S3 bucket
resource "aws_s3_bucket" "dashlearn-tfstate" {
  bucket = "dashlearn-tfstate-s3-9821"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "tfstate-encrypt" {
  bucket = aws_s3_bucket.dashlearn-tfstate.bucket
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_versioning" "versioning_example" {
  bucket = aws_s3_bucket.dashlearn-tfstate.bucket
  versioning_configuration {
    status = "Enabled"
  }
}

#Create DynamoDB
resource "aws_dynamodb_table" "state-lock-table" {
  name         = "state-lock"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"
  attribute {
    name = "LockID"
    type = "S"
  }
}