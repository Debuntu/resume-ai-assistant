resource "aws_cloudwatch_log_group" "lambda_logs" {
  name              = "/aws/lambda/${aws_lambda_function.resume_ai.function_name}"
  retention_in_days = 14
}