resource "aws_iam_role" "iam_for_lambda_pj" {
  name = "iam_for_lambda_pj"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": "AssumeRole"
    }
  ]
}
EOF
}



resource "aws_iam_policy" "iam_for_lambda_pj" {
  name        = "ProjectAWSLambdaExecutionRolePolicy"
  path        = "/"
  description = "Provides write permissions to CloudWatch Logs and S3 buckets"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:*"
            ],
            "Resource": "*"
        }
    ]
}
EOF
}

# Adding S3 bucket as trigger to my lambda and giving the permissions
resource "aws_lambda_permission" "allow_bucket" {
  statement_id  = "AllowExecutionFromS3Bucket"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambdagetfiles.arn
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.bucket_data.arn
}

resource "aws_s3_bucket_notification" "aws-lambda-trigger" {
  bucket = aws_s3_bucket.bucket_data.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.lambdagetfiles.arn
    events              = ["s3:ObjectCreated:*"]
    filter_suffix       = ".csv"
  }

  depends_on = [aws_lambda_permission.allow_bucket]
}

resource "aws_iam_role_policy_attachment" "lambda_attach" {
  role       = aws_iam_role.iam_for_lambda_pj.name
  policy_arn = aws_iam_policy.iam_for_lambda_pj.arn
}
