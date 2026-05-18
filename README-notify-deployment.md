# notify-deployment

## Description

<!-- AUTO-DOC-DESCRIPTION:START - Do not remove or modify this section -->

Sends a deployment notification to configured webhooks.

<!-- AUTO-DOC-DESCRIPTION:END -->

```yaml
- name: Post deployment info
  uses: entur/gha-notify-deployment/.github/actions/notify-deployment@main
  with:
    # Required
    gitdailies-url: ${{ vars.GITDAILIES_WEBHOOK_URL }}
    gitdailies-key: ${{ secrets.GITDAILIES_WEBHOOK_KEY }}
    grafana-url: ${{ vars.GRAFANA_CLOUD_URL }}
    grafana-key: ${{ secrets.GRAFANA_CLOUD_API_TOKEN }}

    # Optional – defaults to GitHub context values
    repo: ${{ github.repository }}        # e.g. "owner/repo"
    branch: ${{ github.ref_name }}        # e.g. "main"
    commit-sha: ${{ github.sha }}         # full commit SHA
    environment: "prd"                    # prd, tst, dev, or sbx
    grafana-annotation-text: ""          # image name/tag or deployment identifier e.g. "my-app:1.2"
    grafana-annotation-tags: ""          # space-separated extra tags for the annotation other than "deployment", repo and environment
    deployment-start-time: ""            # Epoch in milliseconds for when deployment started
    deployment-end-time: ""              # Epoch in milliseconds for when deployment ended
```

## Inputs

<!-- AUTO-DOC-INPUT:START - Do not remove or modify this section -->

|                                                 INPUT                                                 |  TYPE  | REQUIRED |           DEFAULT            |                                                                                DESCRIPTION                                                                                 |
|-------------------------------------------------------------------------------------------------------|--------|----------|------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|                          <a name="input_branch"></a>[branch](#input_branch)                           | string |  false   |  `"${{ github.ref_name }}"`  |                                                                                Branch name                                                                                 |
|                    <a name="input_commit-sha"></a>[commit-sha](#input_commit-sha)                     | string |  false   |    `"${{ github.sha }}"`     |                                                                                 Commit SHA                                                                                 |
|       <a name="input_deployment-end-time"></a>[deployment-end-time](#input_deployment-end-time)       | string |  false   |                              |                                                              Deployment end time, Epoch in <br>milliseconds                                                                |
|    <a name="input_deployment-start-time"></a>[deployment-start-time](#input_deployment-start-time)    | string |  false   |                              |                                                             Deployment start time, Epoch in <br>milliseconds                                                               |
|                   <a name="input_environment"></a>[environment](#input_environment)                   | string |  false   |           `"prd"`            |                                                                Deployment environment (prd, tst, dev, sbx)                                                                 |
|              <a name="input_gitdailies-key"></a>[gitdailies-key](#input_gitdailies-key)               | string |   true   |                              |                                                    Webhook authentication key (pass org secret GITDAILIES_WEBHOOK_KEY)                                                     |
|              <a name="input_gitdailies-url"></a>[gitdailies-url](#input_gitdailies-url)               | string |   true   |                              |                                                      Webhook endpoint URL (pass org variable GITDAILIES_WEBHOOK_URL)                                                       |
| <a name="input_grafana-annotation-tags"></a>[grafana-annotation-tags](#input_grafana-annotation-tags) | string |  false   |                              |                                                         Space-separated extra tags for the <br>Grafana annotation                                                          |
| <a name="input_grafana-annotation-text"></a>[grafana-annotation-text](#input_grafana-annotation-text) | string |  false   |                              | Text body for the Grafana <br>annotation. For images, use image <br>name and tag. For other <br>types, use something that both <br>identifies the deployment and version.  |
|                   <a name="input_grafana-key"></a>[grafana-key](#input_grafana-key)                   | string |   true   |                              |                                                     Grafana Cloud API token (pass org secret GRAFANA_CLOUD_API_TOKEN)                                                      |
|                   <a name="input_grafana-url"></a>[grafana-url](#input_grafana-url)                   | string |   true   |                              |                                                 Grafana Cloud API endpoint URL <br>(pass org variable GRAFANA_CLOUD_URL)                                                   |
|                             <a name="input_repo"></a>[repo](#input_repo)                              | string |  false   | `"${{ github.repository }}"` |                                                                          Repository (owner/repo)                                                                           |

<!-- AUTO-DOC-INPUT:END -->

## Outputs

<!-- AUTO-DOC-OUTPUT:START - Do not remove or modify this section -->
No outputs.
<!-- AUTO-DOC-OUTPUT:END -->
