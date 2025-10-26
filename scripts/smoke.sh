#!/bin/sh
set -e

sleep 5

curl -s http://web:8000/transcriptions/ | jq '. | length'

curl -s -X POST http://web:8000/transcriptions/ \
  -H 'Content-Type: application/json' \
  -d '{"title": "Smoke Test", "text": "hello", "folder": "tests", "topics": ["demo"], "length_sec": 120, "speakers": ["bot"]}'

websocat -t ws://web:8000/ws/notifications/ &
PID=$!
sleep 2
kill $PID || true

curl -s http://web:8000/reco/content/u1 | jq
