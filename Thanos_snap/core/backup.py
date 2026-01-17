from __future__ import annotations
from pathlib import Path
import shutil
from core.utils import stamp

def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)

def backup_file(src: Path, backup_dir: Path) -> Path:
    ensure_dir(backup_dir)
    dst = backup_dir / f"{src.stem}.THANOS_BACKUP_{stamp()}{src.suffix}"
    shutil.copy2(src, dst)
    return dst

def backup_folder_files(files: list[Path], backup_dir: Path) -> Path:
    """
    Copies the CURRENT versions of the files (only those involved in the snap)
    into a timestamped backup folder.
    """
    snap_dir = backup_dir / f"THANOS_FOLDER_BACKUP_{stamp()}"
    ensure_dir(snap_dir)
    for f in files:
        # preserve basename; if collisions occur, you can improve with subdirs later
        shutil.copy2(f, snap_dir / f.name)
    return snap_dir
