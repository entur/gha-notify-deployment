#!/bin/bash

set -eEuo pipefail

payload=$(jq -n \
  --arg kind       "deployed" \
  --arg repository "$REPO" \
  --arg environment "$ENVIRONMENT" \
  --arg branch     "$BRANCH" \
  --arg commitSHA  "$COMMIT_SHA" \
  '{kind: $kind, repo: $repository, environment: $environment, branch: $branch, commitSHA: $commitSHA}')

curl -sSf --max-time 5 -X POST \
  -H "Content-Type: application/json" \
  -H "webhook-key: $GITDAILIES_KEY" \
  -d "$payload" \
  "$GITDAILIES_URL" \
  2>>deployment_notification_errors.log \
  && echo "Notification dispatched to GitDailies" \
  || echo "Failed to send notification to GitDailies, error logged for investigation"
  