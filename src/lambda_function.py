import json
import boto3

bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

MODEL_ID = "anthropic.claude-sonnet-4-20250514-v1:0"


def lambda_handler(event, context):

    body = json.loads(event.get("body", "{}"))

    resume = body.get("resume", "")
    job = body.get("jobDescription", "")

    prompt = f"""
You are an expert technical recruiter.

Compare this resume against the job description.

Resume:
{resume}

Job Description:
{job}

Return ONLY valid JSON with this format:

{{
  "match_score": number,
  "strengths": [],
  "missing_skills": [],
  "professional_summary": "",
  "recommendations": []
}}
"""

    response = bedrock.invoke_model(
        modelId=MODEL_ID,
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ]
        })
    )

    result = json.loads(response["body"].read())

    answer = result["content"][0]["text"]

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": answer
    }