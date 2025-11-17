# Serverless-S3-Compliance-Scanner

## Project Description
This is a serverless S3 compliance scanner that audits encryption, public access, and versioning across all buckets and publishes versioned JSON reports to a secure S3 bucket. This project was
built based on a tutorial built with ChatGPT and Claude.ai.
## Architecture
![diagram](https://github.com/terrythomas00/serverless-S3-compliance-scanner/blob/main/s3_scanner_diagram.png)
## Components Description:
| Component           | Functionality                                                                                                                                  |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| Source S3 Bucket    | A source to upload your images from your local machine                                                                                         |
| Lambda Function     | Invoked whenver an image is dropped into the Source S3 bucket. The Lambda function parses the event, loads source object, and generates output |
| Processed S3 Bucket | A destination where processed images from the lambda function are placed                                                                       |
