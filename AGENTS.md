# Agents

This repository provides reusable GitHub Actions for notifying third-party systems when a deployment occurs. Currently supports GitDailies and Grafana Cloud, with PagerDuty planned.

For Entur AI and agent standards, see https://github.com/entur/ai.

## Project specifics

**Action structure**: The single composite action lives in `.github/actions/notify-deployment/action.yml`. Each notification target has its own bash script under `bash/`. Adding a new target means adding a bash script and a step in `action.yml`.

**Error handling**: All notification steps use `continue-on-error: true` so a failure never blocks the caller's workflow. Curl errors are written to `deployment_notification_errors.log` and forwarded to Sentry by `bash/send_errors_to_sentry.sh`.

**Auto-generated documentation**: `README-notify-deployment.md` is regenerated automatically from `action.yml` by the `auto-doc` workflow on every merge to main. Do not manually edit the `AUTO-DOC-*` sections in that file — edit `action.yml` instead.

**Testing**: Tests use a local mock HTTP server (`testscripts/mock_server.py`) that captures the first inbound request to `captured.json`, then `testscripts/validate.py` asserts the payload fields. To add coverage for a new notification target, update both scripts.

**Commit convention**: This repo uses Conventional Commits (`feat:`, `fix:`, `docs:`, `ci:`, `chore:`, etc.).
