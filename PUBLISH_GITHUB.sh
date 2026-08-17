#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
python3 scripts/bootstrap_github.py --owner six-nut --repo PocketMen-with-you --public --confirm-public --release v0.3.0 --allow-existing
