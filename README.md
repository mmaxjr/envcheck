# envcheck

Small CLI to validate deployment prerequisites before a release.

```text
python envcheck.py --env API_KEY --env DATABASE_URL --file config/production.env
```

The command exits with status 1 and lists missing prerequisites when a check fails.
