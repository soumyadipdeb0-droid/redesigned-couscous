from __future__ import annotations

from dataclasses import dataclass

from agents.resume_agent import CandidateProfile
from utils.embeddings import simple_text_similarity
from utils.scraper import JobPosting


@dataclass
class RankedJob:
    job: JobPosting
    relevance_score: float


class RankingAgent:
    def __init__(self, threshold: float = 0.25, top_k: int = 15):
        self.threshold = threshold
        self.top_k = top_k

    def rank(self, profile: CandidateProfile, jobs: list[JobPosting]) -> list[RankedJob]:
        profile_text = " ".join(profile.roles + profile.skills + [str(profile.experience_years)])
        ranked: list[RankedJob] = []

        for job in jobs:
            job_text = f"{job.title} {job.description} {job.location}"
            score = simple_text_similarity(profile_text, job_text)
            if score >= self.threshold:
                ranked.append(RankedJob(job=job, relevance_score=score))

        ranked.sort(key=lambda x: x.relevance_score, reverse=True)
        return ranked[: self.top_k]
