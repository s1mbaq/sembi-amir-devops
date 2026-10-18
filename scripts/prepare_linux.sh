#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"
mkdir -p app scripts config logs backup evidence
touch logs/application.log
if [ ! -s logs/application.log ]; then
    cat > logs/application.log <<'LOG'
INFO Application started
INFO User logged in
WARNING Configuration file missing
INFO Database connected
ERROR Database connection failed
INFO Application restarted
WARNING Memory usage is high
INFO Request received
ERROR Request failed
INFO Application stopped
LOG
fi
chmod 600 private.txt
chmod 644 public.txt
chmod +x scripts/*.sh
printf 'Project prepared in %s\n' "$ROOT_DIR"
