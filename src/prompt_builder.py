import os


PROMPT_DIR = os.path.join(
    os.path.dirname(__file__),
    "prompts"
)

SUPPORTED_TASKS = [
    "resume_analysis",
    "cover_letter",
    "interview_questions",
    "ats_optimizer"
]

def build_prompt(task, resume, job_description=None):

    if task not in SUPPORTED_TASKS:
      raise ValueError(
        f"Unsupported task '{task}'. "
        f"Available tasks: {SUPPORTED_TASKS}"
      )

    prompt_file = os.path.join(
        PROMPT_DIR,
        f"{task}.txt"
    )

    if not os.path.exists(prompt_file):
        raise ValueError(
            f"Unsupported task: {task}"
        )

    with open(prompt_file, "r") as file:
        template = file.read()


    prompt = template.format(
        resume=resume,
        jobDescription=job_description or ""
    )

    return prompt