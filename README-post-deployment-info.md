# post-deployment-info

## Description

<!-- AUTO-DOC-DESCRIPTION:START - Do not remove or modify this section -->

Sends a deployment notification to a configured webhook endpoint.

<!-- AUTO-DOC-DESCRIPTION:END -->

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

|                               INPUT                               |  TYPE  | REQUIRED |           DEFAULT            |                             DESCRIPTION                              |
|-------------------------------------------------------------------|--------|----------|------------------------------|----------------------------------------------------------------------|
|        <a name="input_branch"></a>[branch](#input_branch)         | string |  false   |  `"${{ github.ref_name }}"`  |                             Branch name                              |
|  <a name="input_commit-sha"></a>[commit-sha](#input_commit-sha)   | string |  false   |    `"${{ github.sha }}"`     |                              Commit SHA                              |
|           <a name="input_repo"></a>[repo](#input_repo)            | string |  false   | `"${{ github.repository }}"` |                       Repository (owner/repo)                        |
| <a name="input_webhook-key"></a>[webhook-key](#input_webhook-key) | string |   true   |                              | Webhook authentication key (pass org secret GITDAILIES_WEBHOOK_KEY)  |
| <a name="input_webhook-url"></a>[webhook-url](#input_webhook-url) | string |   true   |                              |    Webhook endpoint URL (pass org secret GITDAILIES_WEBHOOK_URL)     |

<!-- AUTO-DOC-INPUT:END -->

## Outputs

<!-- AUTO-DOC-OUTPUT:START - Do not remove or modify this section -->
No outputs.
<!-- AUTO-DOC-OUTPUT:END -->
