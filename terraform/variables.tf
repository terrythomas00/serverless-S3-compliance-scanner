variable "bucket_name" {
  description = "The name of the S3 bucket"
  type        = string
}

variable "aws_region" {
  description = "The AWS region where resources will be created"
  type        = string

}

variable "project_name" {
  description = "The name of the project"
  type        = string

}

variable "environment" {
  description = "environment setting"
  type = string
}