#!/bin/bash

set -eEuo pipefail

if [[ -z $END_TIME ]]; then
  END_TIME="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
fi
if [[ -z $START_TIME ]]; then
  START_TIME="$ENTD_TIME"
fi

payload=$(jq -n \
  --arg event       "deployment" \
  --arg start_time  "$(date -u +"%Y-%m-%dT%H:%M:%SZ")" \
  --arg repository  "$REPO" \
  --arg branch      "$BRANCH" \
  --arg commitSHA   "$COMMIT_SHA" \
  --arg environment "$ENVIRONMENT" \
  --arg image       "$IMAGE" \
  '{time: $start_time, timeEnd: $end_time, tags: [$event, $environment, $repository], text: "Deployment of $branch@$commitSHA, image: $image"}')


curl -X POST -H "Content-Type: application/json" \
-H "Authorization: Bearer $GRAFANA_API_TOKEN" \
-d "$payload" "$GRAFANA_URL/api/annotations" \
  2>>deployment_notification_errors.log
