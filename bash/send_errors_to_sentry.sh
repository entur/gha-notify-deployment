#!/bin/bash

set -eEuo pipefail

if [ ! -f deployment_notification_errors.log ] || [ ! -s deployment_notification_errors.log ]; then
    exit 0
fi
sentry_ts=$(date +%s)
curl_error=$(cat deployment_notification_errors.log 2>/dev/null)
sentry_payload=$(jq -n \
    --arg log "$curl_error" \
    '{level:"error", message:"Deployment notification failed", extra:{log:$log}, tags:{action:"notify-deployment"}}')
sentry_response=$(curl -sS --max-time 10 -X POST \
    -H "Content-Type: application/json" \
    -H "X-Sentry-Auth: Sentry sentry_version=7, sentry_key=d31db74544391305f5edcc6a541d25f0, sentry_timestamp=$sentry_ts" \
    -d "$sentry_payload" \
    "https://o4508182734503936.ingest.de.sentry.io/api/4511139252469840/store/")
sentry_event_id=$(echo "$sentry_response" | jq -r '.id')
if [ -n "$sentry_event_id" ] && [ "$sentry_event_id" != "null" ]; then
    echo "Event sent to Sentry for investigation (Event id: $sentry_event_id)"
else
    echo "Failure was not reported to Sentry"
fi
