"""Download Anthropic Claude documentation for the RAG corpus."""
from __future__ import annotations

from pathlib import Path

import httpx

CORPUS_DIR = Path(__file__).parent.parent / "corpus" / "anthropic"

DOCS = [
    ("https://platform.claude.com/docs/en/about-claude/models/overview.md", "models-overview.md"),
    ("https://platform.claude.com/docs/en/about-claude/models/choosing-a-model.md", "choosing-a-model.md"),
    ("https://platform.claude.com/docs/en/about-claude/pricing.md", "pricing.md"),
    ("https://platform.claude.com/docs/en/api/rate-limits.md", "rate-limits.md"),
    ("https://platform.claude.com/docs/en/build-with-claude/context-windows.md", "context-windows.md"),
    ("https://platform.claude.com/docs/en/build-with-claude/embeddings.md", "embeddings.md"),
    ("https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview.md", "tool-use.md"),
    ("https://platform.claude.com/docs/en/intro.md", "intro.md"),
]


def main():
    CORPUS_DIR.mkdir(parents=True, exist_ok=True)
    client = httpx.Client(timeout=30.0, follow_redirects=True)

    for url, filename in DOCS:
        target = CORPUS_DIR / filename
        if target.exists():
            print(f"  Skipping {filename} (already exists)")
            continue

        print(f"  Downloading {filename}...")
        try:
            resp = client.get(url)
            resp.raise_for_status()
            target.write_text(resp.text, encoding="utf-8")
            print(f"    Saved ({len(resp.text)} chars)")
        except Exception as e:
            print(f"    Failed: {e}")

    client.close()

    files = list(CORPUS_DIR.glob("*.md"))
    print(f"\nDone! {len(files)} files in {CORPUS_DIR}")
    for f in sorted(files):
        print(f"  {f.name}")


if __name__ == "__main__":
    main()
