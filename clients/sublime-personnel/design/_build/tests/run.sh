#!/usr/bin/env bash
# Runs every check against the local review server. Start the server first
# (python3 _build/serve.py 8901); this launches its own headless browser.
set -uo pipefail
cd "$(dirname "$0")/../.."
CHS=${CHS:-$HOME/Library/Caches/ms-playwright/chromium_headless_shell-1234/chrome-headless-shell-mac-arm64/chrome-headless-shell}
PORT=${CDP_PORT:-9352}
PROFILE=$(mktemp -d)

curl -sf -o /dev/null http://localhost:8901/index.html || {
  echo "review server is not up — run: python3 _build/serve.py 8901"; exit 1; }

"$CHS" --headless --disable-gpu --hide-scrollbars --window-size=1440,900 \
       --remote-debugging-port="$PORT" --user-data-dir="$PROFILE" about:blank >/dev/null 2>&1 &
BROWSER=$!
trap 'kill $BROWSER 2>/dev/null; rm -rf "$PROFILE"' EXIT
for _ in $(seq 1 20); do curl -sf -o /dev/null "http://127.0.0.1:$PORT/json/version" && break; sleep .3; done

fail=0
for t in links.py pages.mjs industries.mjs images.mjs funnel.mjs jobs.mjs; do
  echo; echo "════ $t"
  case $t in
    *.py)  python3 "_build/tests/$t" ;;
    *.mjs) node "_build/tests/$t" ;;
  esac || fail=1
done
echo; [ $fail -eq 0 ] && echo "ALL SUITES PASS" || echo "SUITE FAILURES"
exit $fail
