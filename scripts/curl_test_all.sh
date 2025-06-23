#!/bin/bash
# Simple health check script for frontend and backend URLs
# Usage: BACKEND=http://localhost:5000 FRONTEND=http://localhost:8000 ./curl_test_all.sh

set -e

BACKEND=${BACKEND:-http://localhost:5000}
FRONTEND=${FRONTEND:-http://localhost:8000}

backend_endpoints=(
  "/auth/register"
  "/auth/login"
  "/products/"
  "/inventory/"
  "/requests/"
  "/orders/"
  "/users/"
)

frontend_paths=(
  "/"
  "/pages/register.html"
  "/pages/manufacturer.html"
  "/pages/cfa.html"
  "/pages/stockist.html"
)

echo "Checking backend endpoints"
for ep in "${backend_endpoints[@]}"; do
  url="$BACKEND$ep"
  printf '%-40s' "$url"
  curl -Ls -o /dev/null -w '%{http_code} -> %{url_effective}\n' "$url"
done

echo ""
echo "Checking frontend pages"
for path in "${frontend_paths[@]}"; do
  url="$FRONTEND$path"
  printf '%-40s' "$url"
  curl -Ls -o /dev/null -w '%{http_code} -> %{url_effective}\n' "$url"
done
