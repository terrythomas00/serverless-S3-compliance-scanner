resource "aws_ecr_repository" "scanner" {
  name                 = "${var.project_name}-repo"
  image_tag_mutability = "MUTABLE" # Set to "IMMUTABLE" if you want to prevent overwriting tags
  image_scanning_configuration {
    scan_on_push = true
  }

  encryption_configuration {
    encryption_type = "AES256" # Use "KMS" if you want to use a custom KMS key
  }
}
