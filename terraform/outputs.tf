output "api_url" {
  value = aws_apigatewayv2_stage.dev.invoke_url
}

output "ecr_repository_url" {
  value = aws_ecr_repository.lambda_repo.repository_url
}