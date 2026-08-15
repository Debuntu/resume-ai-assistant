import json
import logging


from config import LOG_LEVEL
from prompt_builder import build_prompt
from bedrock_client import invoke_claude

# Configure logging
logger = logging.getLogger()
logger.setLevel(LOG_LEVEL)

def lambda_handler(event, context):
    logger.info("Resume analysis request received.")

    try:
        # Parse request body
        body = json.loads(event.get("body", "{}"))

        task = body.get("task")
        resume = body.get("resume")
        job_description = body.get("jobDescription")

        # Validate required fields
        if not task or not resume:
            return {
                "statusCode":400,
                "body":json.dumps({
                "message":
                "task and resume are required"
             })
            }

        logger.info("Building AI prompt...")

        prompt = build_prompt(
            task,
            resume,
            job_description
        )

        logger.info("Invoking Amazon Bedrock...")

        response = invoke_claude(prompt)

        logger.info("Resume analysis completed successfully.")

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": response
        }

    except Exception as e:
        logger.exception("Unhandled exception during resume analysis.")

        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "message": "Internal Server Error",
                "error": str(e)
            })
        }