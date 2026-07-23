from pathlib import Path
from tqdm import tqdm
from core.obsidian_graph import extract_links

CACHE_DIR = Path(".cache")
CACHE_DIR.mkdir(exist_ok=True)

IGNORE_DIRS = {
    ".obsidian",
    "node_modules",
    ".git",
    ".cache",
    ".output"
}


def is_ignored(path: Path) -> bool:
    return any(part in IGNORE_DIRS for part in path.parts) # idk if this relative or absolute path

def load_markdown_files(vault_path):
    vault = Path(vault_path)
    files = list(vault.rglob("*.md"))

    documents = []
    for f in tqdm(files, desc = "Loading notes"):
        if is_ignored(f):
            continue
        
        try:
            text = f.read_text(encoding="utf-8")
            
            links_out = extract_links(text)

            documents.append({
                "path": str(f),
                "text": text,
                "links_out": links_out
            })
        except Exception as e:
            print(f"Skipping {f}: {e}")

    return documents
