
---

# 3. `doc/project-structure.md`

```markdown
# Resume AI Assistant - Project Structure

## Repository Layout

```text
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
│   ├── styles.css
│   └── ...
│
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── github-oidc.tf
│   ├── ...
│   └── backend configuration
│
└── .github/
    └── workflows/
        └── terraform.yml