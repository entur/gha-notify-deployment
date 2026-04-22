#!/bin/bash

set -eEuo pipefail

payload=$(jq -n \
  --arg kind       "deployed" \
  --arg repository "$REPO" \
  --arg branch     "$BRANCH" \
  --arg commitSHA  "$COMMIT_SHA" \
  '{kind: $kind, repo: $repository, branch: $branch, commitSHA: $commitSHA}')

curl -sSf --max-time 10 -w "\nHTTP status: %{http_code}" -X POST \
  -H "Content-Type: application/json" \
  -H "webhook-key: $GITDAILIES_KEY" \
  -d "$payload" \
  "$GITDAILIES_URL" \
  2>>deployment_notification_errors.log