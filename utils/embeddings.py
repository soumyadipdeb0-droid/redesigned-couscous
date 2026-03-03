from __future__ import annotations

import math
from collections import Counter


def simple_text_similarity(a: str, b: str) -> float:
    """Lightweight token-overlap similarity fallback.

    This keeps the MVP dependency-light. Replace with embedding cosine similarity
    via OpenAI or sentence-transformers for production.
    """

    tokens_a = [t for t in a.lower().split() if t]
    tokens_b = [t for t in b.lower().split() if t]
    if not tokens_a or not tokens_b:
        return 0.0

    ca = Counter(tokens_a)
    cb = Counter(tokens_b)

    dot = sum(ca[t] * cb[t] for t in set(ca) & set(cb))
    norm_a = math.sqrt(sum(v * v for v in ca.values()))
    norm_b = math.sqrt(sum(v * v for v in cb.values()))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)
