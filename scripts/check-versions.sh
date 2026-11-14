#!/usr/bin/env bash
# Version consistency now lives in tools/sync-claude-manifests.py: plugins/<id>/plugin.json is the
# one source of a plugin's version and marketplace.json's top-level version is the ecosystem's.
# The tool generates every other copy (README, marketplace entry, Claude and Codex manifests,
# README badge) and its --check also fails when a CHANGELOG top entry disagrees. This wrapper keeps
# `just versions`, CI and mason's auditor pointing at one stable command.
#
# Usage: scripts/check-versions.sh

set -euo pipefail
cd "$(dirname "$0")/.."
exec python3 tools/sync-claude-manifests.py --check
