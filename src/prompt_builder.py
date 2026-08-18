import os


# Keep all prompt templates in the prompts directory.
PROMPT_DIR = os.path.join(
    os.path.dirname(__file__),
    "prompts"
)


# Define the tasks supported by the application.
SUPPORTED_TASKS = [
    "resume_analysis",
    "cover_letter",
    "interview_questions",
    "ats_optimizer"
]


def build_prompt(task, resume, job_description=None):

    # Reject tasks that aren't supported by the application.
    if task not in SUPPORTED_TASKS:
        raise ValueError(
            f"Unsupported task '{task}'. "
            f"Available tasks: {SUPPORTED_TASKS}"
        )

    # Build the path to the selected prompt template.
    prompt_file = os.path.join(
        PROMPT_DIR,
        f"{task}.txt"
    )

    # Make sure the prompt template exists.
    if not os.path.exists(prompt_file):
        raise ValueError(
            f"Prompt file not found for task: {task}"
        )

    # Read the prompt template as UTF-8 text.
    with open(
        prompt_file,
        "r",
        encoding="utf-8"
    ) as file:
        template = file.read()

    # Insert the resume and job description into the template.
    prompt = template.format(
        resume=resume,
        jobDescription=job_description or ""
    )

    return prompt