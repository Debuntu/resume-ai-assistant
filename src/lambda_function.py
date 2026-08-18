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
            logger.warning("Missing required fields.")

            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({
                    "message": "task and resume are required"
                })
            }

        logger.info("Building AI prompt for task: %s", task)

        prompt = build_prompt(
            task,
            resume,
            job_description
        )

        # Invoke Claude through Amazon Bedrock.
        response = invoke_claude(prompt)

        # Log the raw model response so we can diagnose JSON parsing failures.
        logger.info("RAW CLAUDE RESPONSE: %s", response)

        logger.info("Resume analysis completed successfully.")

        # Clean common formatting Claude may add around JSON.
        cleaned_response = response.strip()

        # Remove an opening Markdown JSON code fence.
        if cleaned_response.startswith("```json"):
            cleaned_response = cleaned_response[len("```json"):].strip()

        # Remove a generic Markdown code fence if present.
        elif cleaned_response.startswith("```"):
            cleaned_response = cleaned_response[len("```"):].strip()

        # Remove the closing Markdown code fence.
        if cleaned_response.endswith("```"):
            cleaned_response = cleaned_response[:-3].strip()

        try:
            # Convert Claude's JSON text into a Python object.
            result = json.loads(cleaned_response)

        except json.JSONDecodeError:
            # Log the response so we can diagnose malformed or truncated JSON.
            logger.error(
                "Claude returned invalid JSON: %s",
                cleaned_response
            )

            return {
                "statusCode": 502,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({
                    "message":
                        "AI model returned an invalid response format."
                })
            }
        
        logger.info("Resume analysis completed successfully.")

        # Return structured API response
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "task": task,
                "result": result
            })
        }

    except Exception as e:
        logger.exception(
            "Unhandled exception during resume analysis."
        )

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