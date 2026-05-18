#!/bin/bash

set -eEuo pipefail

if [[ -z $END_TIME ]]; then
  END_TIME="$(date -u +%s%3N)"
fi
if [[ -z $START_TIME ]]; then
  START_TIME="$END_TIME"
fi
TAGS=("test" "this")
payload=$(jq -n \
  --arg event       "deployment" \
  --arg repository  "$REPO" \
  --arg environment "$ENVIRONMENT" \
  --arg text        "$GRAFANA_ANNOTATION_TEXT" \
  --arg tags        "$GRAFANA_ANNOTATION_TAGS" \
  --argjson start_time  "$START_TIME" \
  --argjson end_time    "$END_TIME" \
  '{time: $start_time, timeEnd: $end_time, tags: ([$event, $repository, $environment] + ($tags | split(" ") | map(select(length > 0)))), text: $text}')

curl -sSf --max-time 5 -X POST \
-H "Content-Type: application/json" \
-H "Authorization: Bearer $GRAFANA_API_TOKEN" \
-d "$payload" \
"$GRAFANA_URL/api/annotations" \
  2>>deployment_notification_errors.log \
&& echo "Notification dispatched to Grafana" \
|| echo "Failed to send notification to Grafana, error logged for investigation"
