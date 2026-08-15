# Resume AI Assistant - Project Structure

```
resume-ai-assistant/
│
├── docs/
│   ├── architecture.md
│   └── project-structure.md
│
├── src/
│   ├── lambda_function.py          # Lambda entry point
│   ├── bedrock_client.py           # Amazon Bedrock integration
│   ├── prompt_builder.py           # Loads prompt templates
│   ├── prompts/
│   │   ├── resume_analysis.txt
│   │   ├── cover_letter.txt
│   │   ├── interview_questions.txt
│   │   └── ats_optimizer.txt
│   └── requirements.txt
│
├── terraform/
│   ├── provider.tf
│   ├── variables.tf
│   ├── iam.tf
│   ├── lambda.tf
│   ├── apigateway.tf
│   ├── outputs.tf
│   └── terraform.tfvars
│
├── .gitignore
├── README.md
└── LICENSE
```

## Project Components

### src/

Contains all Lambda application source code.

### prompts/

Stores reusable prompt templates that are loaded dynamically by the application.

Keeping prompts separate from Python code allows prompt updates without modifying business logic.

### terraform/

Contains Infrastructure as Code used to provision AWS resources.

### docs/

Contains architecture and design documentation.