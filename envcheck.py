"""Validate deployment environment variables and configuration files."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

PROFILES = {
    "production": ["DATABASE_URL", "SECRET_KEY"],
    "ci": ["CI"],
}

def validate(required: list[str], files: list[Path], profile: str | None = None) -> list[str]:
    profile_vars = PROFILES.get(profile, []) if profile else []
    errors = [f"Missing environment variable: {name}" for name in (*profile_vars, *required) if not os.environ.get(name)]
    errors.extend(f"Missing configuration file: {path}" for path in files if not path.is_file())
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Check deployment prerequisites")
    parser.add_argument("--env", action="append", default=[], metavar="NAME", help="required environment variable")
    parser.add_argument("--file", action="append", default=[], type=Path, metavar="PATH", help="required configuration file")
    parser.add_argument("--profile", choices=sorted(PROFILES), help="use a predefined deployment profile")
    args = parser.parse_args()
    errors = validate(args.env, args.file, args.profile)
    if errors:
        print("Environment check failed. Fix these prerequisites:")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print("Environment check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
