output "ecr_repo_url" { value = aws_ecr_repository.scanner.repository_url }
output "lambda_name" { value = aws_lambda_function.scanner.function_name }
output "reports_bucket" { value = aws_s3_bucket.reports_bucket }
