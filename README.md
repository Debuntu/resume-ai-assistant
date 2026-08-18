# Resume AI Assistant

An AI-powered resume and job application assistant built using AWS serverless services, Amazon Bedrock, Python, Terraform, and a JavaScript-based customer portal.

The application allows users to provide a resume and job description and use AI to perform different tasks:

- Resume Analysis
- ATS Optimization
- Cover Letter Generation
- Interview Question Generation

The project is also being integrated with GitHub Actions for Infrastructure as Code (IaC) CI/CD using GitHub OIDC and AWS IAM.

---

## Project Goal

The goal of this project is to demonstrate how an AI-powered application can be designed, deployed, and operated using modern AWS and DevOps practices.

Instead of directly interacting with an AI chatbot, this project demonstrates how to build an application around an AI foundation model with:

- A customer-facing web interface
- REST API
- Serverless backend
- Prompt engineering
- Amazon Bedrock integration
- Infrastructure as Code
- Remote Terraform state
- CI/CD
- IAM and OIDC
- CloudWatch logging
- Error handling

The overall technology stack is:

```text
AI Engineering
      +
AWS Cloud
      +
Serverless Architecture
      +
Infrastructure as Code
      +
CI/CD
      +
Security
      +
Observability

User
  |
  v
Customer Portal
HTML / CSS / JavaScript
  |
  | HTTPS POST
  v
Amazon API Gateway
HTTP API
  |
  v
AWS Lambda
Python 3.12
  |
  +--------------------+
  |                    |
  v                    v
Prompt Builder       CloudWatch
  |                    |
  v                    |
Prompt Templates       |
  |                    |
  +--------+-----------+
           |
           v
    Amazon Bedrock
           |
           v
   Anthropic Claude
           |
           v
      JSON Response
           |
           v
      AWS Lambda
           |
           v
     API Gateway
           |
           v
     Customer Portal
           |
           v
          User

See doc/architecture.md for more details

Supported AI Tasks


| Task                | Prompt File               | Description                                                   |
| ------------------- | ------------------------- | ------------------------------------------------------------- |
| Resume Analysis     | `resume_analysis.txt`     | Compares a resume against a job description                   |
| ATS Optimization    | `ats_optimizer.txt`       | Identifies ATS keywords, gaps, and optimization opportunities |
| Cover Letter        | `cover_letter.txt`        | Generates a customized professional cover letter              |
| Interview Questions | `interview_questions.txt` | Generates technical and role-specific interview questions     |

resume-ai-assistant/
│
├── README.md
│
├── doc/
│   ├── architecture.md
│   └── project-structure.md
│
├── src/
│   ├── lambda_function.py
│   ├── bedrock_client.py
│   ├── config.py
│   ├── prompt_builder.py
│   │
│   └── prompts/
│       ├── resume_analysis.txt
│       ├── ats_optimizer.txt
│       ├── cover_letter.txt
│       └── interview_questions.txt
│
├── frontend/
│   ├── index.html
│   ├── app.js
│   └── ...
│
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── ...
│   └── backend configuration
│
└── .github/
    └── workflows/
        └── terraform.yml

See doc/project-structure.md for more details

Prerequisites

Install the following tools:

AWS CLI
Terraform
Python 3.12
Git
Web browser
AWS account
GitHub account

Verify the installations:

# Verify Python version.
python3 --version

# Verify Terraform installation.
terraform version

# Verify AWS CLI installation.
aws --version

# Verify Git installation.
git --version

# Configure AWS credentials and default region.
aws configure

Region:
us-east-1

# Confirm the AWS identity currently being used.
aws sts get-caller-identity

Amazon Bedrock

The application uses Amazon Bedrock to access Anthropic Claude.

The currently tested working inference profile is:

global.anthropic.claude-haiku-4-5-20251001-v1:0

The model configuration is stored in: src/config.py

# Bedrock model/inference profile used by Lambda.
MODEL_ID = "global.anthropic.claude-haiku-4-5-20251001-v1:0"

# Maximum number of tokens requested from the model.
MAX_TOKENS = 4096

Model availability can vary by AWS account and region.

Check available inference profiles:

# List Bedrock inference profiles available in us-east-1.
aws bedrock list-inference-profiles --region us-east-1

Source Code:

The Lambda application is located under: src/

The main components are:

lambda_function.py

Main Lambda entry point.

Responsibilities include:

Parsing API Gateway requests
Validating input
Selecting the requested AI task
Building prompts
Invoking Bedrock
Parsing model responses
Returning HTTP responses
Logging errors
prompt_builder.py

Responsible for selecting the correct prompt template.

Supported tasks: 
resume_analysis
cover_letter
interview_questions
ats_optimizer

bedrock_client.py

Handles communication with Amazon Bedrock.

config.py

Contains application configuration such as:

Bedrock model ID
Maximum tokens
Logging configuration
prompts/

Contains the individual prompt templates.

Keeping prompts separate from application code makes prompt engineering easier and prevents the Lambda function from becoming tightly coupled to individual AI tasks.

API

The application exposes an HTTP API through Amazon API Gateway.

Endpoint:
POST /analyze

The exact API Gateway URL is generated by Terraform after deployment.

API Request

Example:

{
  "task": "resume_analysis",
  "resume": "AWS Terraform Kubernetes Python",
  "jobDescription": "Looking for AWS Terraform Kubernetes GitHub Actions"
}

API Response

Example:

{
  "task": "resume_analysis",
  "result": {
    "match_score": 75,
    "strengths": [
      "AWS experience matches job requirement",
      "Terraform experience matches job requirement",
      "Kubernetes experience matches job requirement"
    ],
    "missing_skills": [
      "GitHub Actions - not mentioned in resume"
    ],
    "professional_summary": "Candidate has strong infrastructure-as-code and container orchestration skills.",
    "recommendations": [
      "Assess ability to quickly learn GitHub Actions",
      "Ask about automation and pipeline experience"
    ]
  }
}

Deploying Infrastructure with Terraform

Move into the Terraform directory: 
cd terraform
terraform init
terraform fmt
terraform validate
terraform plan
terraform apply

Get the API Endpoint: 

after terraform apply, run terraform output and get the endpoint, something like - 

https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/analyze

Test the API with cURL

Example: 

# Test the resume analysis API.
curl -X POST https://YOUR_API_ID.execute-api.us-east-1.amazonaws.com/analyze \
-H "Content-Type: application/json" \
-d '{
  "task":"resume_analysis",
  "resume":"AWS Terraform Kubernetes Python",
  "jobDescription":"Looking for AWS Terraform Kubernetes GitHub Actions"
}'

You can replace the short test resume with a complete resume and the job description with a real job posting.

Running the Customer Portal

The frontend is located under: fronted/

Navigate to the directory first : 

cd frontend

# Serve the frontend over HTTP for local development.
python3 -m http.server 8000

open http://localhost:8000 on your browser, don't directly open the index.html file because browsers may assign the page a null origin and cause CORS failures.

Customer Portal

The customer portal provides:

AI task selection
Resume input
Job description input
Analyze button
AI response display

The UI dynamically changes the input fields based on the selected task.

CORS

The API Gateway HTTP API is configured for CORS so that the local frontend can communicate with the API.

The recommended local development URL is:

http://localhost:8000

CloudWatch Logging

Lambda logs are sent to Amazon CloudWatch.

Logs are particularly useful for troubleshooting:

Bedrock errors
IAM permission problems
Invalid model responses
Invalid JSON
Lambda exceptions
API request failures

Example:

Lambda
   |
   v
CloudWatch Logs
   |
   v
Troubleshooting

The Lambda function logs the raw AI response when JSON parsing fails, which helps diagnose model-output issues.

Known Limitation

The AI prompts instruct Claude to return valid JSON.

However, large model responses can occasionally:

Include Markdown code fences
Return malformed JSON
Become truncated
Contain unexpected formatting

This has been observed with the cover-letter and interview-question tasks.

Resume Analysis and ATS Optimization have been successfully tested.

Improving model-response parsing and adding response-repair/retry logic is a planned enhancement.

GitHub Actions CI/CD

The project is being integrated with GitHub Actions.

The intended workflow is:

Developer
    |
    | git push
    v
GitHub
    |
    v
GitHub Actions
    |
    v
GitHub OIDC
    |
    v
AWS IAM Role
    |
    v
Terraform
    |
    +--> terraform init
    |
    +--> terraform fmt
    |
    +--> terraform validate
    |
    +--> terraform plan
    |
    +--> terraform apply
    |
    v
AWS Infrastructure

The GitHub Actions IAM role is:

resume-ai-github-actions-role

The AWS GitHub OIDC provider has already been created and imported into Terraform state.

The OIDC trust relationship is currently being finalized.

GitHub Actions Security

GitHub Actions is designed to authenticate to AWS using OIDC instead of storing long-lived AWS access keys.

The workflow uses:

permissions:
  id-token: write
  contents: read

GitHub obtains a short-lived OIDC token and AWS STS uses it to assume the configured IAM role.

This is preferable to storing:

AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY

as GitHub repository secrets.

Destroying AWS Resources

Because this project is primarily a learning and portfolio project, AWS resources should be destroyed when they are not being used.

From the Terraform directory:

# Destroy AWS resources managed by Terraform.
terraform destroy

Confirm with:

yes

Important:

Do not delete the Terraform S3 state bucket.

The application resources can be destroyed while the Terraform state backend remains available.

Redeploying After Destroy

When development resumes:

# Move into the Terraform directory.
cd terraform


# Initialize Terraform using the existing S3 remote backend.
terraform init


# Review infrastructure changes.
terraform plan


# Recreate the AWS infrastructure.
terraform apply
Troubleshooting
Internal Server Error

Check Lambda CloudWatch logs.

Possible causes:

Bedrock model access
IAM permissions
Invalid model ID
Invalid inference profile
Lambda exception
Invalid model response
Bedrock AccessDeniedException

Check the available inference profiles:

# Check available Bedrock inference profiles.
aws bedrock list-inference-profiles \
  --region us-east-1

Make sure the configured model is active and authorized for the AWS account.

Invalid AI Response Format

If Lambda reports:

AI model returned an invalid response format

check CloudWatch logs.

The Lambda logs the raw model response when JSON parsing fails.

Common causes:

```json
{
   ...
}


or:


```text
Incomplete JSON response

or:

Unexpected model output
GitHub Actions OIDC Error

If GitHub Actions reports:

Not authorized to perform sts:AssumeRoleWithWebIdentity

check:

GitHub OIDC provider
IAM role trust policy
Repository name
GitHub OIDC subject claim
AWS account
IAM role ARN
Future Improvements
 Complete GitHub Actions OIDC configuration
 Replace broad IAM permissions with least-privilege policies
 Add Terraform plan approval
 Improve AI JSON response handling
 Add retry and response-repair logic
 Fix remaining cover-letter response parsing issues
 Fix remaining interview-question response parsing issues
 Add automated API tests
 Add authentication/authorization
 Deploy the frontend
 Add production monitoring
 Add development and production environments
 Add security scanning to CI/CD
Technologies
Cloud
AWS
Amazon API Gateway
AWS Lambda
Amazon Bedrock
Amazon S3
AWS IAM
Amazon CloudWatch
AI
Anthropic Claude
Prompt Engineering
Generative AI
Development
Python 3.12
HTML
CSS
JavaScript
Infrastructure
Terraform
CI/CD
GitHub
GitHub Actions
GitHub OIDC

Author

Debashish Talukder

Cloud / DevOps Engineer

This project was created as a hands-on demonstration of AWS cloud engineering, serverless architecture, Infrastructure as Code, CI/CD, and AI application development.






