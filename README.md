#Test API

curl -X POST https://YOUR_API/analyze \
-H "Content-Type: application/json" \
-d '{
  "task":"{your_task_name}",
  "resume":"AWS Terraform Kubernetes Python",
  "jobDescription":"Looking for AWS Terraform Kubernetes GitHub Actions"
}'