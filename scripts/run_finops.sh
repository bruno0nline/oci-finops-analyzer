#!/bin/bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.."

echo "▶️ OCI FinOps Analyzer – Execução completa"

if [[ ! -f .venv/bin/activate ]]; then
    python3 -m venv .venv
fi
source .venv/bin/activate
python3 -m pip install -r requirements.txt

python3 src/oci_metrics_cpu_mem_media_ndays.py "$@"
