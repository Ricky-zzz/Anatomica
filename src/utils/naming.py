from datetime import datetime
import re


def slugify(text: str, max_words: int = 4) -> str:
    """Creates a concise filename-safe slug from a clinical text."""
    clean = re.sub(r"[^\w\s-]", "", text.lower())
    words = clean.split()[:max_words]
    slug = "-".join(words)
    return slug or "patient-face"


def generate_result_filename(description: str, ext: str = "png") -> str:
    """Generates timestamped slug filename like 2026-11-22_210000_jaundice-pallor.png"""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    slug = slugify(description)
    return f"{timestamp}_{slug}.{ext}"
