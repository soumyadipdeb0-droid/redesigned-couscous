from __future__ import annotations

from typing import List

from agents.resume_agent import CandidateProfile
from utils.scraper import JobPosting, provider_factory


class SearchAgent:
    def __init__(self, provider_name: str, max_results_per_query: int = 25):
        self.provider = provider_factory(provider_name)
        self.max_results_per_query = max_results_per_query

    @staticmethod
    def generate_queries(profile: CandidateProfile) -> List[str]:
        queries = []
        for role in profile.roles:
            for location in profile.preferred_locations:
                queries.append(f"{role} {location} {profile.experience_years} years experience")
        return queries

    def fetch_jobs(self, queries: list[str]) -> list[JobPosting]:
        collected: list[JobPosting] = []
        for query in queries:
            collected.extend(self.provider.search(query, self.max_results_per_query))
        return collected
