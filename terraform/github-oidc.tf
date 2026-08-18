# Allow GitHub Actions to authenticate to AWS using OIDC.
resource "aws_iam_openid_connect_provider" "github" {
  url = "https://token.actions.githubusercontent.com"

  # GitHub's OIDC certificate thumbprint.
  thumbprint_list = [
    "6938fd4d98bab03faadb97b34396831e3780aea1"
  ]

  # Allow GitHub Actions to request AWS credentials.
  client_id_list = [
    "sts.amazonaws.com"
  ]
}

# IAM role assumed by GitHub Actions through OIDC.
resource "aws_iam_role" "github_actions" {
  name = "resume-ai-github-actions-role"

  # Trust policy restricts who can assume this role.
  assume_role_policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Principal = {
          Federated = aws_iam_openid_connect_provider.github.arn
        }

        Action = "sts:AssumeRoleWithWebIdentity"

        Condition = {
          StringEquals = {
            "token.actions.githubusercontent.com:aud" = "sts.amazonaws.com"
          }

          # Only your GitHub repository can assume this role.
          StringLike = {
            "token.actions.githubusercontent.com:sub" = "repo:Debuntu/resume-ai-assistant:*"
          }
        }
      }
    ]
  })
}

# Grant Terraform permissions needed to manage this project.
# We can tighten these permissions later using least privilege.
resource "aws_iam_role_policy_attachment" "github_actions_admin" {
  role = aws_iam_role.github_actions.name

  policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess"
}