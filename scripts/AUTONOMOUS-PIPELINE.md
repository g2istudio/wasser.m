# WasserMarket autonomous pipeline

The pipeline joins official-site discovery, official-domain filtering, duplicate
checks, deterministic extraction, evidence validation and website publication.
It does not call an AI model. Supported detection includes Shopware, Shopify,
WooCommerce, Magento, PrestaShop, BigCommerce and generic Product JSON-LD.
Official PDF manuals linked directly from a product page are parsed as an
additional evidence source when product-page specifications are incomplete.

Safety rules:

- only domains in `official_brand_domains.json` are processed;
- accessories and replacement filters are rejected before extraction;
- existing Wasser.Market brand/model identities are skipped;
- every published field needs verbatim evidence from the official product page
  or an official manual linked directly from that page;
- ambiguous values remain empty;
- only `PUBLISH_READY` records can reach the site importer;
- source hashes make publication idempotent.

Install the versioned runtime:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/install-autonomous-agent.ps1
```

Run the complete pipeline without publishing:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run-autonomous-agent.ps1
```

Enable publication only after reviewing the dry-run report:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run-autonomous-agent.ps1 -Publish
```

Logs are appended to
`%TEMP%\wasser-market-autonomous-pipeline.log` and the existing publisher log.
