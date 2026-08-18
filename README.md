#Test API

curl -X POST https://YOUR_API/analyze \
-H "Content-Type: application/json" \
-d '{
  "task":"{your_task_name}",
  "resume":"AWS Terraform Kubernetes Python",
  "jobDescription":"Looking for AWS Terraform Kubernetes GitHub Actions"
}'

#test front end locally

#run ths in your local terminal from fronend directory and from your browser open http://localhost:8000

python3 -m http.server 8000

