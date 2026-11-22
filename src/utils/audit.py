import json
from pathlib import Path
from typing import Any, Dict


def save_audit_log(audit_path: Path, data: Dict[str, Any]) -> None:
    """Serializes audit trail data to a formatted JSON file."""
    audit_path.parent.mkdir(parents=True, exist_ok=True)
    with open(audit_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, default=str)
