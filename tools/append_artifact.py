import json
import sys
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_LEDGER = Path("external_artifacts.jsonl")


def append_artifact(
    source: str,
    summary: str,
    artifact_type: str = "external_ai_discussion",
    ledger_path: Path = DEFAULT_LEDGER,
) -> None:
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "type": artifact_type,
        "source": source,
        "summary": summary,
    }
    with ledger_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
    print(f"✅ Appended artifact to {ledger_path}: {source}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python append_artifact.py <source_url> <summary...>")
        sys.exit(1)

    source_url = sys.argv[1]
    summary_text = " ".join(sys.argv[2:])
    append_artifact(source_url, summary_text)
