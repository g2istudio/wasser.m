# Agent pilot import

The website is static. Its protected delivery channel is the GitHub API for
`g2istudio/wasser.m`; merges to `main` trigger the existing FTPS workflow.
There is no public writable HTTP endpoint on wasser.market.

`python scripts/import-agent-test.py` imports exactly the two reviewed records
in `data/agent-test-products.json`. The payload was exported programmatically
from `C:/wasser-market-agent/data/wasser_market.db`, local product IDs 1 and 45.
The importer does not read credentials, modify that database, or publish itself.
Upload generated files atomically to a separate GitHub branch, review the diff,
then merge. Keep API credentials outside repository files and browser code.

Identity policy:
- Update `waterdrop-umkehrosmoseanlage-g3p800`, preserving the German offer,
  EUR price and regional specs. Do not modify the MNR35 bundle.
- Create/update `osmofresh-fusion-pro-2`. Do not overwrite Fusion Pro.
- The pilot refuses other models. Repeat execution must produce identical files.

Only reviewed fields are imported. Unsupported GPD, tank, UV and stage evidence
from the original extraction is excluded. Waterdrop's 32.4 pounds in a kg-named
field and its US price are not transferred to the German offer. Product fields,
evidence, original source URLs, units and checked date are retained in
`agent_import` on the two catalog records. The pages display source evidence.
These are manufacturer statements, not independent certification verification.

The existing image and brand logo are retained for the German Waterdrop offer.
Fusion Pro 2 uses the agent's manufacturer image (Jet Black), separately from
the site's brand logo. It currently depends on the manufacturer's image hosting.

Stop after the two-product pilot. Do not enable mass import until extraction
quality, region/variant mapping and evidence semantics have been addressed.
