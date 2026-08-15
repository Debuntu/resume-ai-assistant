import json
import boto3

from config import MODEL_ID, MAX_TOKENS

bedrock = boto3.client(
    "bedrock-runtime",
    region_name="us-east-1"
)


def invoke_claude(prompt):

    response = bedrock.invoke_model(
        modelId=MODEL_ID,
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": MAX_TOKENS,
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

    return result["content"][0]["text"]