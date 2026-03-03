from __future__ import annotations

import smtplib
from email.message import EmailMessage
from pathlib import Path

from agents.ranking_agent import RankedJob


class EmailAgent:
    def __init__(self, smtp_host: str, smtp_port: int, username: str, password: str):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.username = username
        self.password = password

    @staticmethod
    def build_digest(ranked_jobs: list[RankedJob]) -> str:
        lines = ["Top matching jobs today:\n"]
        for i, rj in enumerate(ranked_jobs, start=1):
            lines.append(
                f"{i}. {rj.job.title} — {rj.job.company} ({rj.job.location})\n"
                f"   score={rj.relevance_score:.3f}\n"
                f"   {rj.job.job_link}"
            )
        return "\n".join(lines)

    def send(self, *, from_email: str, to_email: str, subject: str, body: str, attachment_path: str | None = None) -> None:
        msg = EmailMessage()
        msg["From"] = from_email
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.set_content(body)

        if attachment_path:
            file_path = Path(attachment_path)
            msg.add_attachment(
                file_path.read_bytes(),
                maintype="text",
                subtype="csv",
                filename=file_path.name,
            )

        with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
            server.starttls()
            server.login(self.username, self.password)
            server.send_message(msg)
