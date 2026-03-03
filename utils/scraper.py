from __future__ import annotations

import os
from dataclasses import dataclass, asdict
from datetime import date
from typing import Iterable, List


@dataclass
class JobPosting:
    title: str
    company: str
    location: str
    job_link: str
    description: str
    posted_date: str
    source: str

    def as_dict(self) -> dict:
        return asdict(self)


class BaseProvider:
    def search(self, query: str, max_results: int = 25) -> List[JobPosting]:
        raise NotImplementedError


class MockProvider(BaseProvider):
    """Local deterministic provider for offline development/testing."""

    def search(self, query: str, max_results: int = 25) -> List[JobPosting]:
        jobs = [
            JobPosting(
                title="Data Scientist",
                company="Acme Analytics",
                location="Remote",
                job_link="https://example.com/jobs/acme-ds",
                description="Python, SQL, machine learning, experimentation.",
                posted_date=str(date.today()),
                source="mock",
            ),
            JobPosting(
                title="ML Engineer",
                company="Rocket AI",
                location="Bangalore",
                job_link="https://example.com/jobs/rocket-ml",
                description="Deploy ML models, Docker, AWS, Python.",
                posted_date=str(date.today()),
                source="mock",
            ),
        ]
        return jobs[:max_results]


class SerpApiProvider(BaseProvider):
    """SerpAPI provider placeholder.

    Implement live Google Jobs retrieval with serpapi package.
    """

    def search(self, query: str, max_results: int = 25) -> List[JobPosting]:
        api_key = os.getenv("SERPAPI_API_KEY")
        if not api_key:
            raise RuntimeError("SERPAPI_API_KEY is required for serpapi provider")

        # Placeholder to keep MVP runnable without hard dependency.
        # Replace with real API call in production.
        return []


def provider_factory(name: str) -> BaseProvider:
    if name == "mock":
        return MockProvider()
    if name == "serpapi":
        return SerpApiProvider()
    raise ValueError(f"Unsupported provider: {name}")


def dedupe_jobs(jobs: Iterable[JobPosting]) -> list[JobPosting]:
    seen = set()
    unique = []
    for job in jobs:
        key = (job.title.strip().lower(), job.company.strip().lower(), job.location.strip().lower())
        if key in seen:
            continue
        seen.add(key)
        unique.append(job)
    return unique
