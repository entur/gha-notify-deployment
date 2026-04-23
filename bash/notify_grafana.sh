#!/bin/bash

set -eEuo pipefail

if [[ -z $END_TIME ]]; then
  END_TIME="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
fi
if [[ -z $START_TIME ]]; then
  START_TIME="$ENTD_TIME"
fi
MESSAGE_TEXT="Deployment of $BRANCH@$COMMIT_SHA"
if [[ -n $IMAGE ]]; then
  MESSAGE_TEXT="$MESSAGE_TEXT, image: $IMAGE"
fi

payload=$(jq -n \
  --arg event       "deployment" \
  --arg repository  "$REPO" \
  --arg environment "$ENVIRONMENT" \
  --arg text        "$MESSAGE_TEXT" \
  --arg start_time  "$START_TIME" \
  --arg end_time    "$END_TIME" \
  '{time: $start_time, timeEnd: $end_time, tags: [$event, $environment, $repository], text: $text}')


curl -sSf --max-time 5 -X POST -H "Content-Type: application/json" \
-H "Authorization: Bearer $GRAFANA_API_TOKEN" \
-d "$payload" "$GRAFANA_URL/api/annotations" \
  2>>deployment_notification_errors.log \
&& echo "Notification dispatched to Grafana" \
|| echo "Failed to send notification to Grafana, error logged for investigation"
