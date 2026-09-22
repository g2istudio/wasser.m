# Automatic WasserMarket Agent import

The import is deterministic and does not call a language model. It reads only
records whose `status` and `quality_status` are both `PUBLISH_READY`.

Run a preview without changing files:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/agent-auto-publish.ps1 -DryRun
```

Import, validate, commit and push up to ten changed records:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/agent-auto-publish.ps1
```

The importer rejects records without supported field evidence, a unique HTTPS
primary image, an existing brand page, or an unambiguous identity. Imported
source hashes are stored in `data/agent-import-state.json`; unchanged records
are skipped. A push to `main` uses the existing FTPS deployment workflow.
