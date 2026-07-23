"""Keyword search over loka.com, with a bundled offline fallback.

Fetches a few loka.com pages live and searches their text. If the network is
unavailable, falls back to the snapshot in loka_website_cache.json.

Rebuild the snapshot with:
    uv run python shared/website.py --refresh
"""

import html
import json
import re
from pathlib import Path

try:
    import httpx
except ImportError:
    httpx = None

LOKA_PAGES = [
    "https://www.loka.com/",
    "https://www.loka.com/about",
    "https://www.loka.com/services",
    "https://www.loka.com/careers",
]

_CACHE_PATH = Path(__file__).with_name("loka_website_cache.json")
_TIMEOUT = 8.0
_HEADERS = {"User-Agent": "Mozilla/5.0 (loka-workshop-demo)"}


def _strip_html(raw: str) -> str:
    raw = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", raw)
    raw = re.sub(r"(?s)<[^>]+>", " ", raw)
    return re.sub(r"\s+", " ", html.unescape(raw)).strip()


def _fetch_live() -> dict[str, str]:
    """Fetch the pages from loka.com; raise on any failure."""
    if httpx is None:
        raise RuntimeError("httpx not available")
    pages: dict[str, str] = {}
    with httpx.Client(follow_redirects=True, timeout=_TIMEOUT, headers=_HEADERS) as client:
        for url in LOKA_PAGES:
            resp = client.get(url)
            if resp.status_code == 200:
                text = _strip_html(resp.text)
                if text:
                    pages[url] = text
    if not pages:
        raise RuntimeError("no pages fetched")
    return pages


def _get_pages() -> tuple[dict[str, str], str]:
    """Return (pages, source) where source is 'live' or 'cache (offline)'."""
    try:
        return _fetch_live(), "live"
    except Exception:
        return json.loads(_CACHE_PATH.read_text(encoding="utf-8")), "cache (offline)"


def _tokenize(text: str) -> set[str]:
    return {w.strip(".,!?;:()\"'") for w in text.lower().split() if len(w.strip(".,!?;:()\"'")) > 2}


def _chunks(text: str, size_words: int = 45) -> list[str]:
    words = text.split()
    return [" ".join(words[i:i + size_words]) for i in range(0, len(words), size_words)]


def search_website(query: str, top_k: int = 3) -> str:
    """Search loka.com and return the best-matching passages (with source URLs).

    Notes whether the results came from a live fetch or the offline cache.
    """
    pages, source = _get_pages()
    query_tokens = _tokenize(query)

    scored: list[tuple[int, str, str]] = []
    for url, text in pages.items():
        for chunk in _chunks(text):
            overlap = len(query_tokens & _tokenize(chunk))
            if overlap:
                scored.append((overlap, url, chunk))
    scored.sort(key=lambda item: item[0], reverse=True)
    top = scored[:top_k]

    if not top:
        return f"No matches on loka.com for '{query}'. (source: {source})"

    blocks = [f"[{url}]\n{chunk}" for _, url, chunk in top]
    return f"(source: {source})\n\n" + "\n\n".join(blocks)


def refresh_cache() -> dict[str, str]:
    """Fetch live and overwrite the offline snapshot."""
    pages = _fetch_live()
    _CACHE_PATH.write_text(json.dumps(pages, indent=1, ensure_ascii=False), encoding="utf-8")
    return pages


if __name__ == "__main__":
    import sys

    if "--refresh" in sys.argv:
        cached = refresh_cache()
        print(f"Cached {len(cached)} pages ({sum(len(t) for t in cached.values())} chars) "
              f"to {_CACHE_PATH.name}\n")

    print(search_website("what services does Loka offer?"))
