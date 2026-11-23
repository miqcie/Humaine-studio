#!/bin/bash
# Load the TypeSafe key from 1Password (never printed), then run qa.py.
# usage: design-system/birds/qa.sh run openai30 [--dry-run] | report openai30 | calibrate
set -euo pipefail
. ~/scripts/op-service-env.sh >/dev/null 2>&1 || true
key="$(op read 'op://Developer Vault/TYPESAFE_API_KEY_CLAUDE/credential')"
export TYPESAFE_API_KEY="$key"
cd "$(dirname "$0")"
exec uv run --quiet --with 'typesafe-sdk>=0.7.5,<0.8.0' --with pillow python qa.py "$@"
