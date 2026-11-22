from pathlib import Path


def ensure_directory(path: Path) -> Path:
    """Ensures a directory exists, creating parents if necessary."""
    path.mkdir(parents=True, exist_ok=True)
    return path
