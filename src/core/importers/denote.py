from pathlib import Path
import re

from core.obsidian_graph import extract_links

DENOTE_PATTERN = re.compile(
    r"(?P<date>\d{8}T\d{6})--(?P<title>[^_]+)(?P<tags>__.*)?"
)

def parse_filename(path: Path):
    name = path.stem

    match = DENOTE_PATTERN.match(name)

    if not match:
        return {
            "title": name,
            "tags": [],
            "date": None
        }

    title = match.group("title")

    tags_raw = match.group("tags")
    tags = []

    if tags_raw:
        tags = [t for t in tags_raw.split("__") if t]

    return {
        "title": title,
        "tags": tags,
        "date": match.group("date")
    }

def import_denote(vault_path: str):
    vault = Path(vault_path)
    files = list(vault.rglob("*.org"))

    documents = []
    
    for f in files:
        try:
            text = f.read_text(encoding="utf-8")
            meta = parse_filename(f)

            documents.append({
                "path": str(f),
                "text": text,
                "links_out": [],
                "metadata": {
                    "source": "denote",
                    **meta
                    }
            })
        except Exception as e:
            print(f"Skipping {f}: {e}")

    return documents

