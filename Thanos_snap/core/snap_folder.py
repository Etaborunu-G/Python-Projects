from __future__ import annotations
from pathlib import Path
from typing import Optional, Sequence
import os

from send2trash import send2trash

from core.utils import SnapPlan, unbiased_sample

def list_candidate_files(folder: Path, allowed_exts: Optional[Sequence[str]]) -> list[Path]:
    """
    allowed_exts:
      - None => all files
      - list of extensions like ['.png','.txt']
    """
    files: list[Path] = []
    for item in folder.iterdir():
        try:
            if not item.is_file() or item.is_symlink():
                continue
            if allowed_exts is None:
                files.append(item)
            else:
                if item.suffix.lower() in allowed_exts:
                    files.append(item)
        except Exception:
            continue
    return sorted(files)

def make_plan(folder: Path, strength_percent: int, allowed_exts: Optional[Sequence[str]]) -> SnapPlan:
    files = list_candidate_files(folder, allowed_exts)
    total = len(files)
    to_remove = (total * strength_percent) // 100
    chosen = unbiased_sample(files, to_remove)
    preview = [p.name for p in chosen[:30]]
    return SnapPlan(total=total, to_remove=to_remove, targets_preview=preview)

def execute(folder: Path, strength_percent: int, allowed_exts: Optional[Sequence[str]], progress_cb=None) -> tuple[int, int]:
    """
    Deletes chosen files to Recycle Bin/Trash (NOT permanent).
    Returns: (deleted_ok, failed)
    """
    files = list_candidate_files(folder, allowed_exts)
    total = len(files)
    to_remove = (total * strength_percent) // 100
    chosen = unbiased_sample(files, to_remove)

    deleted_ok = 0
    failed = 0
    for idx, f in enumerate(chosen, start=1):
        try:
            send2trash(str(f))
            deleted_ok += 1
        except Exception:
            failed += 1
        if progress_cb:
            progress_cb(idx, to_remove)
    return deleted_ok, failed
