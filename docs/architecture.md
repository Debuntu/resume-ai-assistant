# Resume AI Assistant Architecture

## High-Level Architecture

```
               Customer Portal (Coming Next)
                         │
                         ▼
                 Amazon API Gateway
                         │
                         ▼
                 AWS Lambda (Python)
                         │
         ┌───────────────┴────────────────┐
         │                                │
         ▼                                ▼
 prompt_builder.py             bedrock_client.py
         │                                │
         ▼                                ▼
 Prompt Templates               Amazon Bedrock Runtime
         │                                │
         ▼                                ▼
resume_analysis.txt            Claude Haiku 4.5
cover_letter.txt
interview_questions.txt
ats_optimizer.txt
                         │
                         ▼
                  JSON Response
```

---

## AWS Resources

- Amazon API Gateway
- AWS Lambda
- Amazon Bedrock
- Anthropic Claude Haiku 4.5
- AWS IAM
- Amazon CloudWatch Logs

Provisioned using Terraform.

---

## Application Flow

1. Client submits resume and job description.
2. API Gateway receives the HTTP request.
3. Lambda validates the payload.
4. Prompt Builder loads the required prompt template.
5. Prompt Builder injects user input into the template.
6. Bedrock Client invokes Anthropic Claude through Amazon Bedrock.
7. Claude returns structured JSON.
8. Lambda returns the response through API Gateway.

---

## Prompt Library

Current prompt templates include:

- Resume Analysis
- Cover Letter Generation
- Interview Question Generation
- ATS Resume Optimization

The application is designed so additional prompt templates can be added without modifying the Lambda entry point.