#!/usr/bin/env python3
"""Make root landing pages work with or without a trailing slash."""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
PAGES = ("brands.html", "community.html", "products.html", "professionals.html")


def absolute_root_attributes(source):
    pattern = re.compile(
        r'(?P<prefix>\b(?:href|src|action)=["\'])(?P<url>[^"\']+)(?P<suffix>["\'])',
        re.I,
    )

    def replace(match):
        url = match.group("url")
        if url.startswith(("#", "/", "?", "http:", "https:", "mailto:", "tel:", "data:")):
            return match.group(0)
        if url in (".", "./"):
            url = "/"
        else:
            url = "/" + url.removeprefix("./")
        return match.group("prefix") + url + match.group("suffix")

    return pattern.sub(replace, source)


for name in PAGES:
    path = ROOT / name
    path.write_text(absolute_root_attributes(path.read_text(errors="ignore")))

print(f"Normalized root-relative assets and links on {len(PAGES)} landing pages")
