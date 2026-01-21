#!/usr/bin/env bash
# Simple health check script for the Secure Flower Store backend.
set -euo pipefail

# This script pings the health endpoint of the API to ensure it is responding.
URL="${HEALTH_URL:-http://localhost:8000/health}"

echo "Checking health at $URL"
if curl -fsS "$URL" > /dev/null; then
  echo "OK"
  exit 0
else
  echo "Health check failed"
  exit 1
fi
