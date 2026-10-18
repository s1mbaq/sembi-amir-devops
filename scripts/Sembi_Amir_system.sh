#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
INFO_FILE="$ROOT_DIR/Sembi_Amir_info.txt"
printf '==============================\nStudent Information\n==============================\n'
if [ -f "$INFO_FILE" ]; then
    cat "$INFO_FILE"
    printf 'Student information file exists.\n'
else
    printf 'Student information file does not exist.\n'
fi
printf '==============================\nSystem Information\n==============================\n'
printf 'Username: '; whoami
printf 'Hostname: '; hostname
printf 'Current Date: '; date
printf 'Operating System: '; uname -a
printf 'Disk Usage:\n'; df -h "$ROOT_DIR"
printf 'Memory Usage:\n'
if command -v free >/dev/null 2>&1; then
    free -h
else
    printf 'Run this script inside the provided Linux container to use free.\n'
fi
