data "archive_file" "lambda_zip" {
  type = "zip"

  source_dir = "../src"

  output_path = "../src/lambda.zip"
}

resource "aws_lambda_function" "resume_ai" {
  function_name = "resume-ai-assistant"

  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  role    = aws_iam_role.lambda_role.arn
  handler = "lambda_function.lambda_handler"
  runtime = "python3.12"

  timeout     = 30
  memory_size = 256

  environment {
    variables = {
      MODEL_ID   = "global.anthropic.claude-haiku-4-5-20251001-v1:0"
      LOG_LEVEL  = "INFO"
      MAX_TOKENS = "1000"
    }
  }
}