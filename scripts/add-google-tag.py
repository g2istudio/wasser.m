#!/usr/bin/env python3
"""Install exactly one Google tag immediately after <head> on every page."""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
MEASUREMENT_ID = "G-XYC4SQT8L5"
TAG = f'''
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={MEASUREMENT_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());

  gtag('config', '{MEASUREMENT_ID}');
</script>
'''

external = re.compile(
    rf'\s*<!--\s*Google tag \(gtag\.js\)\s*-->\s*'
    rf'<script\b[^>]*src=["\']https://www\.googletagmanager\.com/gtag/js\?id={re.escape(MEASUREMENT_ID)}["\'][^>]*></script>',
    re.I,
)
inline = re.compile(
    rf'\s*<script\b[^>]*>.*?gtag\(\s*["\']config["\']\s*,\s*["\']{re.escape(MEASUREMENT_ID)}["\']\s*\);.*?</script>',
    re.I | re.S,
)

updated = 0
for path in sorted(ROOT.rglob("*.html")):
    source = path.read_text(errors="ignore")
    source = external.sub("", source)
    source = inline.sub("", source)
    source, count = re.subn(r"(<head\b[^>]*>)", r"\1" + TAG, source, count=1, flags=re.I)
    if count != 1:
        raise RuntimeError(f"Missing or duplicate <head> element: {path}")
    path.write_text(source)
    updated += 1

print(f"Installed {MEASUREMENT_ID} on {updated} HTML pages")
