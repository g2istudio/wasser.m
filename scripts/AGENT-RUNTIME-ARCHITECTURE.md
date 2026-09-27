# WasserMarket Agent runtime

The production runtime is a standalone Python process. It has no OpenAI or
Codex dependency. Codex is used only to change and test its source code.

## Pipeline

1. Brave Search discovers brands, official domains, catalogs and product URLs.
2. Ordinary HTTP and JSON-LD extraction run first.
3. A browser is used when the initial HTML is insufficient.
4. Firecrawl is the last fetch fallback for inaccessible or dynamic content.
5. The deterministic commerce parser extracts known fields.
6. Gemini receives at most 12,000 characters of relevant fragments when the
   deterministic result is ambiguous, conflicting, low-confidence or unmapped.
7. Formal validation assigns `DATA_VERIFIED`, `PUBLISH_READY` or
   `NEEDS_REVIEW`.
8. Only `PUBLISH_READY` records can reach the existing protected publisher.

Discovery, extraction, validation and publication are independent commands.
Mass discovery therefore never implies mass publication.

## Module map

- `crawler/discovery.py` and `crawler/candidate_worker.py`: discover brands,
  product URLs and model candidates.
- `crawler/http_collector.py` and `crawler/page_collector.py`: fetch and cache
  source pages.
- `extractor/commerce_parser.py`: orchestrate deterministic field extraction.
- `extractor/category_rules.py`: classify technology and installation from
  source-backed rules.
- `extractor/taxonomy.py` and `config/product_profiles.json`: category profiles,
  required field groups and publication evidence thresholds.
- `crawler/semantic_policy.py`: decide whether conflicts or missing evidence
  justify semantic resolution.
- `semantic_resolution.py` and `sources/gemini_client.py`: send only selected
  fragments to Gemini when the deterministic stages cannot resolve a fact.
- `extractor/validation.py`, `extractor/verification.py` and
  `extractor/publication.py`: validate facts and assign the publication state.
- `sources/wasser_market_api.py` and `scripts/agent-auto-import.py`: protected
  API and deterministic site publication.

New categories and their minimum evidence thresholds should normally be added
to `config/product_profiles.json`. Parser code changes remain necessary only
when the source introduces a new representation that existing generic rules do
not understand.

## Stored layers

- `source_snapshots`: immutable raw and normalized source content, HTTP
  metadata, fetch time and SHA-256 content hash.
- `facts`: every extracted value with source URL, verbatim evidence, method,
  deterministic confidence, parser version and schema version.
- `products`: the current card assembled from validated facts.

`unmapped_attributes` preserves new characteristics. Gemini may propose a
normalized field, but it cannot change production taxonomy or schema.

`canonical_products` separates normalized model identity from optional
variants. Model spelling removes punctuation, so `G3P800`, `G3 P800` and
`G3-P800` resolve to one model. Variant identity remains separate.

## Commands

After `scripts/install-autonomous-agent.ps1` installs the tracked runtime:

```powershell
C:\wasser-market-agent\wasser-agent.cmd discover-brands --region germany
C:\wasser-market-agent\wasser-agent.cmd discover --brand Waterdrop --category reverse-osmosis
C:\wasser-market-agent\wasser-agent.cmd process --brand Waterdrop --model G3P800
C:\wasser-market-agent\wasser-agent.cmd process-pending --limit 10
C:\wasser-market-agent\wasser-agent.cmd reprocess --schema-version 3
C:\wasser-market-agent\wasser-agent.cmd costs
```

Publication selects the direct protected API when `WASSER_MARKET_API_URL`,
`WASSER_MARKET_API_KEY` and `WASSER_MARKET_API_SECRET` are configured. Requests
use HTTPS, a bearer key, an HMAC-SHA256 signature, timestamp, nonce and the
idempotency key `canonical_product_id + card_version`. Until the site exposes
that endpoint, `--transport git` keeps the existing protected GitHub/deploy
path:

```powershell
C:\wasser-market-agent\wasser-agent.cmd publish --status PUBLISH_READY --transport git
```

Use `--no-allow-gemini` before the subcommand to disable semantic fallback.
Provider and runtime ceilings are available on each processing command:

```powershell
C:\wasser-market-agent\wasser-agent.cmd process-pending `
  --max-brave-queries 5 `
  --max-http-requests 50 `
  --max-firecrawl-credits 5 `
  --max-gemini-tokens 20000 `
  --max-products 10 `
  --max-runtime 900
```

When a ceiling is reached, the job receives `BUDGET_STOPPED`. Its database
checkpoint, snapshots and facts remain available for `resume` or `reprocess`.

## Publication safety

Unknown product types, unresolved conflicts, missing critical fields and
unmapped characteristics stay in `NEEDS_REVIEW`. Conflicting facts are retained
instead of overwritten. Repeated publication uses the existing import state and
canonical product identity to avoid duplicate cards.
