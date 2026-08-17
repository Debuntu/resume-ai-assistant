import os

MODEL_ID = os.getenv(
    "MODEL_ID",
    "global.anthropic.claude-haiku-4-5-20251001-v1:0"
)

LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO"
)

MAX_TOKENS = int(
    os.getenv(
        "MAX_TOKENS",
        "2000"
    )
)