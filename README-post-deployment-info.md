# post-deployment-info

## Usage

Sends a deployment notification to a configured webhook endpoint after a successful deployment.

```yaml
- name: Post deployment info
  uses: entur/gha-gitdailies/.github/actions/post-deployment-info
  with:
    # Required
    webhook-url: ${{ secrets.WEBHOOK_URL }}
    webhook-key: ${{ secrets.WEBHOOK_KEY }}

    # Optional – defaults to GitHub context values
    repo: ${{ github.repository }}       # e.g. "owner/repo"
    branch: ${{ github.ref_name }}       # e.g. "main"
    commit-sha: ${{ github.sha }}        # full commit SHA
```

## Inputs

<!-- AUTO-DOC-INPUT:START - Do not remove or modify this section -->

|    INPUT    |  TYPE  | REQUIRED |           DEFAULT            |                         DESCRIPTION                         |
|-------------|--------|----------|------------------------------|-------------------------------------------------------------|
|   branch    | string |  false   |  `"${{ github.ref_name }}"`  |                         Branch name                         |
| commit-sha  | string |  false   |    `"${{ github.sha }}"`     |                         Commit SHA                          |
|    dummy    | string |  false   |                              |          Dummy input to trigger workflow dispatch           |
|    repo     | string |  false   | `"${{ github.repository }}"` |                   Repository (owner/repo)                   |
| webhook-key | string |   true   |                              | Webhook authentication key (pass org secret<br>WEBHOOK_KEY) |
| webhook-url | string |   true   |                              |    Webhook endpoint URL (pass org secret<br>WEBHOOK_URL)    |

<!-- AUTO-DOC-INPUT:END -->

## Outputs

<!-- AUTO-DOC-OUTPUT:START - Do not remove or modify this section -->
No outputs.
<!-- AUTO-DOC-OUTPUT:END -->
