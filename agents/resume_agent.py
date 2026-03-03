from __future__ import annotations

import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List


@dataclass
class CandidateProfile:
    roles: List[str]
    skills: List[str]
    experience_years: int
    preferred_locations: List[str]
    companies: List[str]
    seniority: str


ROLE_PATTERNS = [
    "data scientist",
    "machine learning engineer",
    "ml engineer",
    "data analyst",
    "ai engineer",
]

SKILL_PATTERNS = [
    "python",
    "sql",
    "machine learning",
    "deep learning",
    "pytorch",
    "tensorflow",
    "nlp",
    "llm",
    "aws",
    "docker",
]


class ResumeAgent:
    """Parses resume text and heuristically builds a candidate profile.

    LLM-backed parsing can be added later by swapping `parse_profile`.
    """

    def extract_text(self, resume_path: str) -> str:
        path = Path(resume_path)
        if not path.exists():
            raise FileNotFoundError(f"Resume not found: {resume_path}")

        # MVP: plain text input is supported directly. PDF/DOCX extraction can be
        # integrated with pdfplumber/PyMuPDF/python-docx when needed.
        return path.read_text(encoding="utf-8", errors="ignore")

    def parse_profile(self, resume_text: str, preferred_locations: list[str] | None = None) -> CandidateProfile:
        text = resume_text.lower()

        roles = [r.title() for r in ROLE_PATTERNS if r in text]
        if not roles:
            roles = ["Data Scientist", "ML Engineer"]

        skills = [s.title() for s in SKILL_PATTERNS if s in text]

        years_match = re.findall(r"(\d{1,2})\+?\s+years", text)
        experience_years = max([int(y) for y in years_match], default=0)

        seniority = "Mid-Senior" if experience_years >= 4 else "Junior-Mid"

        profile = CandidateProfile(
            roles=roles,
            skills=skills,
            experience_years=experience_years,
            preferred_locations=preferred_locations or ["Remote"],
            companies=["Product", "Tech"],
            seniority=seniority,
        )
        return profile

    @staticmethod
    def to_json(profile: CandidateProfile) -> str:
        return json.dumps(asdict(profile), indent=2)
