terraform {
  # Store Terraform state centrally in S3 for CI/CD.
  backend "s3" {
    bucket = "terrabucket-deba"
    key    = "resume-ai-assistant/terraform.tfstate"
    region = "us-east-1"

    # Encrypt the state file at rest.
    encrypt = true
  }
}