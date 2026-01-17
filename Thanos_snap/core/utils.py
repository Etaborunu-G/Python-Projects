from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, List, Optional
import random

_rng = random.SystemRandom()

def stamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")

def confirm_phrase_ok(s: str) -> bool:
    return s.strip().lower() == "i am inevitable"

def unbiased_sample(items: List[Path], k: int) -> List[Path]:
    if k <= 0:
        return []
    if k >= len(items):
        return list(items)
    return list(_rng.sample(items, k))

def normalize_exts(exts: Iterable[str]) -> List[str]:
    out = []
    for e in exts:
        e = e.strip()
        if not e:
            continue
        if not e.startswith("."):
            e = "." + e
        out.append(e.lower())
    return sorted(set(out))

@dataclass
class SnapPlan:
    total: int
    to_remove: int
    targets_preview: List[str]
