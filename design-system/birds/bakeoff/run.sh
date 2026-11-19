#!/bin/bash
# Load the Recraft key from 1Password (never printed), then run the bake-off.
# usage: design-system/birds/bakeoff/run.sh <run.py args>
set -euo pipefail
. ~/scripts/op-service-env.sh >/dev/null 2>&1 || true
token="$(op read 'op://Claude Agent/RECRAFT_API_KEY/credential')"
export RECRAFT_API_TOKEN="$token"
cd "$(dirname "$0")"
exec uv run --quiet --with pillow --with numpy --with scipy --with fonttools --with brotli python run.py "$@"
