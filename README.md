# envcheck

Small CLI to validate deployment prerequisites before a release.

```text
python envcheck.py --env API_KEY --env DATABASE_URL --file config/production.env
python envcheck.py --profile production --file config/production.env
```

The built-in `production` profile checks `DATABASE_URL` and `SECRET_KEY`; `ci`
checks `CI`. Add `--env` or `--file` for project-specific requirements. The
command exits with status 1 and lists every missing prerequisite.
