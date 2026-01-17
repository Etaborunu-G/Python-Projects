from __future__ import annotations
from pathlib import Path
from typing import Literal
from core.utils import SnapPlan, unbiased_sample
import random

_rng = random.SystemRandom()

Mode = Literal["lines", "chars"]

def make_plan(file_path: Path, strength_percent: int, mode: Mode) -> SnapPlan:
    data = file_path.read_text(encoding="utf-8", errors="replace")

    if mode == "lines":
        lines = data.splitlines(keepends=True)
        total = len(lines)
        to_remove = (total * strength_percent) // 100
        idxs = list(range(total))
        chosen = set(_rng.sample(idxs, to_remove)) if to_remove > 0 else set()
        preview = []
        # preview first few removed lines (trimmed)
        for i in sorted(list(chosen))[:10]:
            preview.append(lines[i].strip()[:80])
        return SnapPlan(total=total, to_remove=to_remove, targets_preview=preview)

    # chars mode
    total = len(data)
    to_remove = (total * strength_percent) // 100
    return SnapPlan(total=total, to_remove=to_remove, targets_preview=["(character-level removal preview omitted)"])

def execute(file_path: Path, strength_percent: int, mode: Mode, progress_cb=None) -> tuple[int, int]:
    """
    Permanently edits the file content (not sent to trash).
    Returns: (removed_count, kept_count)
    """
    data = file_path.read_text(encoding="utf-8", errors="replace")

    if mode == "lines":
        lines = data.splitlines(keepends=True)
        total = len(lines)
        to_remove = (total * strength_percent) // 100
        if total == 0 or to_remove <= 0:
            return 0, total

        idxs = list(range(total))
        delete_set = set(_rng.sample(idxs, to_remove))

        kept = []
        for i, line in enumerate(lines):
            if i not in delete_set:
                kept.append(line)
            if progress_cb:
                progress_cb(i + 1, total)

        new_data = "".join(kept)
        file_path.write_text(new_data, encoding="utf-8", errors="replace")
        return to_remove, total - to_remove

    # chars mode
    total = len(data)
    to_remove = (total * strength_percent) // 100
    if total == 0 or to_remove <= 0:
        return 0, total

    delete_positions = set(_rng.sample(range(total), to_remove))
    out_chars = []
    for i, ch in enumerate(data):
        if i not in delete_positions:
            out_chars.append(ch)
        if progress_cb and (i % 2000 == 0):
            progress_cb(i + 1, total)

    new_data = "".join(out_chars)
    file_path.write_text(new_data, encoding="utf-8", errors="replace")
    return to_remove, total - to_remove
