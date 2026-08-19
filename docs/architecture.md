# Resume AI Assistant - Architecture

## 1. Application Architecture

The Resume AI Assistant uses a serverless AWS architecture.

```mermaid
flowchart LR

    User["User"]

    subgraph Frontend["Customer Portal"]
        UI["HTML / CSS / JavaScript"]
    end

    subgraph AWS["AWS Cloud - us-east-1"]

        API["Amazon API Gateway<br/>HTTP API"]

        Lambda["AWS Lambda<br/>Python 3.12"]

        PromptBuilder["Prompt Builder<br/>prompt_builder.py"]

        Prompts["Prompt Templates<br/>*.txt"]

        Bedrock["Amazon Bedrock"]

        Claude["Anthropic Claude<br/>Haiku 4.5"]

        Logs["Amazon CloudWatch<br/>Lambda Logs"]
    end

    User --> UI

    UI -->|"HTTPS POST /analyze"| API

    API -->|"Invoke Lambda"| Lambda

    Lambda -->|"Build prompt"| PromptBuilder

    PromptBuilder -->|"Load template"| Prompts

    Prompts -->|"Return template"| PromptBuilder

    PromptBuilder -->|"Final prompt"| Lambda

    Lambda -->|"InvokeModel"| Bedrock

    Bedrock --> Claude

    Claude --> Bedrock

    Bedrock -->|"AI response"| Lambda

    Lambda -->|"Application logs"| Logs

    Lambda -->|"JSON response"| API

    API -->|"HTTP response"| UI

    UI --> User
```

---

## 2. Application Request Flow

The application follows this request and response flow:

```text
                         USER
                           |
                           v
                  +------------------+
                  | Customer Portal  |
                  | HTML/CSS/JS      |
                  +--------+---------+
                           |
                           | POST /analyze
                           v
                  +------------------+
                  |  API Gateway     |
                  |    HTTP API      |
                  +--------+---------+
                           |
                           | Invoke
                           v
                  +------------------+
                  |   AWS Lambda     |
                  |   Python 3.12    |
                  +--------+---------+
                           |
                           | Validate request
                           v
                  +------------------+
                  | Prompt Builder   |
                  | prompt_builder.py|
                  +--------+---------+
                           |
                           | Select prompt
                           v
                  +------------------+
                  | Prompt Template  |
                  |    *.txt         |
                  +--------+---------+
                           |
                           | Final prompt
                           v
                  +------------------+
                  | Amazon Bedrock   |
                  +--------+---------+
                           |
                           | InvokeModel
                           v
                  +------------------+
                  | Anthropic Claude |
                  |    Haiku 4.5     |
                  +--------+---------+
                           |
                           | AI response
                           v
                  +------------------+
                  |   AWS Lambda     |
                  | Parse JSON       |
                  +--------+---------+
                           |
                           | JSON response
                           v
                  +------------------+
                  |  API Gateway     |
                  +--------+---------+
                           |
                           | HTTP response
                           v
                  +------------------+
                  | Customer Portal  |
                  | Display result   |
                  +------------------+
```

## 3. Supported AI Tasks

The application currently supports four tasks:

- resume_analysis
- cover_letter
- interview_questions
- ats_optimizer

The corresponding prompt files at src/prompts/ are:

- resume_analysis.txt
- cover_letter.txt
- interview_questions.txt
- ats_optimizer.txt

## 4. Prompt Architecture

The application separates prompt templates from application code.

```mermaid
flowchart TD

    Request["API Request"]

    Lambda["lambda_function.py"]

    Builder["prompt_builder.py"]

    Analysis["resume_analysis.txt"]
    Cover["cover_letter.txt"]
    Interview["interview_questions.txt"]
    ATS["ats_optimizer.txt"]

    Bedrock["Amazon Bedrock"]

    Request --> Lambda

    Lambda --> Builder

    Builder --> Analysis
    Builder --> Cover
    Builder --> Interview
    Builder --> ATS

    Analysis --> Bedrock
    Cover --> Bedrock
    Interview --> Bedrock
    ATS --> Bedrock
```

This approach makes it possible to modify prompts without changing the core Lambda application logic.

## 5. Lambda Architecture

The Lambda application is divided into separate responsibilities.


```text
lambda_function.py
        |
        +---- config.py
        |
        +---- prompt_builder.py
        |
        +---- bedrock_client.py
                    |
                    v
             Amazon Bedrock
```

lambda_function.py acts as the application controller.

Responsibilities:

- Parse API Gateway event
- Validate input
- Determine task
- Build prompt
- Invoke Bedrock
- Parse response
- Return HTTP response
- Log errors

prompt_builder.py

Responsible for:

- Validating supported tasks
- Locating prompt templates
- Reading prompt files
- Injecting resume/job-description data

bedrock_client.py

Responsible for:

- Creating the Bedrock Runtime client
- Building the model request
- Invoking the model
- Returning the model response

config.py

Centralizes configuration.

## 6. Customer Portal

The customer portal is currently a lightweight frontend built with:

- HTML
- CSS
- JavaScript

The portal communicates directly with API Gateway.


```text
Browser
   |
   | HTTPS
   v
API Gateway

```

During local development it is served using:

Run a local HTTP server for the frontend.
python3 -m http.server 8000

The frontend is accessed through:

http://localhost:8000

## 7. API Gateway

Amazon API Gateway exposes the backend endpoint:

POST /analyze

The API uses an HTTP API and Lambda proxy integration.


```text
Customer Portal
      |
      v
API Gateway HTTP API
      |
      v
AWS Lambda

```

CORS is configured so that the local frontend can call the API.

## 8. Amazon Bedrock

The Lambda function uses Amazon Bedrock Runtime to invoke Anthropic Claude.

Current tested model/inference profile:

global.anthropic.claude-haiku-4-5-20251001-v1:0

The model is configured through:

src/config.py

The application does not hardcode AWS access keys.

Lambda accesses Bedrock using its IAM execution role.

## 9. Logging and Monitoring

```mermaid
flowchart LR

    Lambda["AWS Lambda"]

    CloudWatch["Amazon CloudWatch Logs"]

    Developer["Developer"]

    Lambda --> CloudWatch

    CloudWatch --> Developer
```

Lambda logs are sent to Amazon CloudWatch.

CloudWatch logs are used for:

- Application debugging
- Bedrock errors
- IAM errors
- JSON parsing errors
- API failures
- Unexpected exceptions

The Lambda function logs the raw model response when the response cannot be parsed as JSON.

## 10. Infrastructure as Code

AWS infrastructure is managed using Terraform.

```mermaid
flowchart LR

    Lambda["AWS Lambda"]

    CloudWatch["Amazon CloudWatch Logs"]

    Developer["Developer"]

    Lambda --> CloudWatch

    CloudWatch --> Developer
```

The Terraform configuration provisions resources such as:

- API Gateway
- Lambda
- IAM roles
- IAM policies
- Lambda permissions
- CORS configuration
- GitHub OIDC integration
- GitHub Actions IAM role

Terraform provides repeatable infrastructure deployment.

## 11. Terraform Remote State

```mermaid
flowchart LR

    Lambda["AWS Lambda"]

    CloudWatch["Amazon CloudWatch Logs"]

    Developer["Developer"]

    Lambda --> CloudWatch

    CloudWatch --> Developer
```

Terraform state is stored in Amazon S3.

The S3 backend provides a centralized state location shared between local Terraform execution and CI/CD.

The backend uses:

#Store Terraform state remotely in S3.
backend "s3" {
  bucket = "YOUR-TERRAFORM-STATE-BUCKET"
  key    = "resume-ai-assistant/terraform.tfstate"
  region = "us-east-1"


  #Encrypt state at rest.
  encrypt = true
}

## 12. CI/CD Architecture

The intended CI/CD architecture is:

```mermaid
flowchart LR

    Developer["Developer"]

    GitHub["GitHub Repository<br/>resume-ai-assistant"]

    Actions["GitHub Actions"]

    OIDC["GitHub OIDC"]

    IAM["AWS IAM<br/>GitHub Actions Role"]

    Terraform["Terraform"]

    S3["S3 Remote State"]

    AWS["AWS Infrastructure"]

    Developer -->|"git push"| GitHub

    GitHub --> Actions

    Actions --> OIDC

    OIDC --> IAM

    IAM --> Terraform

    Terraform --> S3

    Terraform --> AWS
```

## 13. CI/CD Workflow

The planned GitHub Actions workflow is:


```text
git push
    |
    v
GitHub Actions
    |
    +--> Checkout
    |
    +--> Setup Terraform
    |
    +--> Configure AWS Credentials
    |       |
    |       +--> GitHub OIDC
    |       |
    |       +--> AWS IAM Role
    |
    +--> Terraform Init
    |
    +--> Terraform Format Check
    |
    +--> Terraform Validate
    |
    +--> Terraform Plan
    |
    +--> Terraform Apply
    |
    v
AWS Infrastructure
```

## 14. GitHub OIDC Security Model

The project uses GitHub OIDC instead of long-lived AWS access keys.


```text

    GitHub Actions
      |
      | OIDC Token
      v
AWS STS
      |
      | AssumeRoleWithWebIdentity
      v
AWS IAM Role
      |
      v
Temporary AWS Credentials
      |
      v
Terraform
```

The GitHub OIDC provider already exists in AWS:

arn:aws:iam::949100095136:oidc-provider/token.actions.githubusercontent.com

The Terraform configuration manages the GitHub Actions IAM role.

The trust relationship is currently being finalized because the GitHub Actions workflow encountered: Not authorized to perform sts:AssumeRoleWithWebIdentity

## 15. IAM Security

The architecture uses IAM roles instead of embedding AWS credentials.

Lambda:

```text
Lambda
  |
  v
Lambda Execution Role
  |
  v
Amazon Bedrock

GitHub Actions:

GitHub Actions
  |
  v
OIDC
  |
  v
IAM Role
  |
  v
Terraform / AWS
```

A future improvement is to replace broad permissions with least-privilege policies.

## 16. Resource Lifecycle

The project is intentionally designed so that AWS resources can be destroyed when not actively being used.

Normal development lifecycle:

```text
terraform apply
      |
      v
Develop / Test
      |
      v
terraform destroy
      |
      v
AWS resources removed
```

The Terraform S3 state backend remains available.

When development resumes:

```text
terraform init
      |
      v
terraform plan
      |
      v
terraform apply
```

## 17. Current Implementation Status

| Component | Status |
|---|---|
| Customer Portal | Working locally |
| API Gateway | Working |
| Lambda | Working |
| Bedrock Integration | Working |
| Resume Analysis | Working |
| ATS Optimization | Working |
| Cover Letter | Needs response-format improvement |
| Interview Questions | Needs response-format improvement |
| CORS | Working |
| CloudWatch Logging | Working |
| Terraform | Working |
| S3 Remote State | Configured |
| GitHub OIDC Provider | Configured |
| GitHub Actions IAM Role | Created |
| GitHub Actions OIDC Authentication | Needs trust-policy fix |
| Automated CI/CD | In progress |

## 18. Future Architecture Improvements

Potential future improvements include:

Current:

```text
Frontend
   |
API Gateway
   |
Lambda
   |
Bedrock
```
Future:

```text
Frontend
   |
   v
CloudFront / Static Hosting
   |
   v
API Gateway
   |
   v
Lambda
   |
   +----> Bedrock
   |
   +----> CloudWatch
   |
   +----> Application metrics
```

Potential additions:

- Authentication
- CloudFront
- S3 frontend hosting
- WAF
- API throttling
- Structured logging
- Automated testing
- Model response validation
- Retry logic
- Dead-letter handling
- Separate dev/prod environments
- Least-privilege IAM
