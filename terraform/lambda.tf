resource "aws_lambda_function" "scanner" {
  function_name = "${var.project_name}-fn"
  role          = aws_iam_role.lambda_exec_role.arn
  package_type  = "Image"
  image_uri     = "${aws_ecr_repository.scanner.repository_url}:lambda-arm64-fix3"
  architectures = ["arm64"]
  timeout = 60
  memory_size = 512

  environment {
    variables = {
      REPORTS_BUCKET = aws_s3_bucket.reports_bucket.bucket
      # OPENAI_API_KEY optional at runtime, not stored in TF.
      AI_SECRET_NAME = "ai-api-key"
      ENABLE_AI = "true"
    }
  }
}
