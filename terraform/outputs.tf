output "lambda_name" {
  value = aws_lambda_function.resume_ai.function_name
}

output "lambda_arn" {
  value = aws_lambda_function.resume_ai.arn
}

output "api_endpoint" {
  value = aws_apigatewayv2_api.resume_api.api_endpoint
}

output "github_actions_role_arn" {
  description = "IAM role assumed by GitHub Actions through OIDC"
  value       = aws_iam_role.github_actions.arn
}