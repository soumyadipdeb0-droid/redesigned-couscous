from __future__ import annotations

import argparse
import csv
import os
from datetime import date
from pathlib import Path

import json

from agents.email_agent import EmailAgent
from agents.ranking_agent import RankingAgent
from agents.resume_agent import ResumeAgent
from agents.search_agent import SearchAgent
from utils.scraper import dedupe_jobs


def load_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_ranked_csv(csv_path: str, ranked_jobs: list) -> None:
    Path(csv_path).parent.mkdir(parents=True, exist_ok=True)
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["date_found", "title", "company", "location", "relevance_score", "link", "source"],
        )
        writer.writeheader()
        today = str(date.today())
        for rj in ranked_jobs:
            writer.writerow(
                {
                    "date_found": today,
                    "title": rj.job.title,
                    "company": rj.job.company,
                    "location": rj.job.location,
                    "relevance_score": f"{rj.relevance_score:.4f}",
                    "link": rj.job.job_link,
                    "source": rj.job.source,
                }
            )


def run_pipeline(resume_path: str, config_path: str) -> str:
    cfg = load_config(config_path)

    resume_agent = ResumeAgent()
    resume_text = resume_agent.extract_text(resume_path)
    profile = resume_agent.parse_profile(
        resume_text,
        preferred_locations=cfg.get("candidate", {}).get("preferred_locations", ["Remote"]),
    )

    search_cfg = cfg.get("search", {})
    search_agent = SearchAgent(
        provider_name=search_cfg.get("provider", "mock"),
        max_results_per_query=search_cfg.get("max_results_per_query", 25),
    )

    queries = search_agent.generate_queries(profile)
    jobs = search_agent.fetch_jobs(queries)
    unique_jobs = dedupe_jobs(jobs)

    ranking_cfg = cfg.get("ranking", {})
    ranking_agent = RankingAgent(
        threshold=ranking_cfg.get("similarity_threshold", 0.25),
        top_k=ranking_cfg.get("top_k", 15),
    )
    ranked = ranking_agent.rank(profile, unique_jobs)

    csv_path = cfg.get("output", {}).get("csv_path", "data/jobs.csv")
    write_ranked_csv(csv_path, ranked)

    email_cfg = cfg.get("email", {})
    if email_cfg.get("enabled", False):
        email_agent = EmailAgent(
            smtp_host=email_cfg["smtp_host"],
            smtp_port=int(email_cfg["smtp_port"]),
            username=os.getenv("SMTP_USERNAME", ""),
            password=os.getenv("SMTP_PASSWORD", ""),
        )
        digest = email_agent.build_digest(ranked)
        email_agent.send(
            from_email=email_cfg["from_email"],
            to_email=email_cfg["to_email"],
            subject="Daily Job Digest",
            body=digest,
            attachment_path=csv_path,
        )

    return csv_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Autonomous Job Search Agent")
    parser.add_argument("--resume", required=True, help="Path to resume text/PDF placeholder")
    parser.add_argument("--config", default="config.json", help="Path to JSON config")
    args = parser.parse_args()

    output_csv = run_pipeline(args.resume, args.config)
    print(f"Pipeline complete. Results written to: {output_csv}")
