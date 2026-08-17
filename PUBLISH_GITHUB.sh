#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 scripts/bootstrap_github.py --owner six-nut --repo PocketMen-with-you --public --confirm-public --release v0.1.0
echo
echo "Done. Upload assets/social-preview.png in GitHub Settings > Social preview."
