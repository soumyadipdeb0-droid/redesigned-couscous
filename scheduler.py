from __future__ import annotations

from main import run_pipeline


# Simple scheduler entrypoint; pair with cron/system scheduler.
if __name__ == "__main__":
    run_pipeline(resume_path="sample_resume.txt", config_path="config.json")
