'''A validation script to check the contents of the captured webhook payload.'''
import json
import sys


def main():
    '''Read the captured payload from the mock server and validate its contents.'''
    with open("captured.json", encoding="UTF-8") as f:
        data = json.load(f)

    print("Captured payload:")
    print(json.dumps(data, indent=2))

    errors = []

    if data.get("kind") != "deployed":
        errors.append(f"kind: expected 'deployed', got '{data.get('kind')}'")
    if data.get("repo") != "test-org/test-repo":
        errors.append(f"repo: expected 'test-org/test-repo', got '{data.get('repo')}'")
    if data.get("branch") != "test-branch":
        errors.append(f"branch: expected 'test-branch', got '{data.get('branch')}'")
    if data.get("commitSHA") != "abc123def456":
        errors.append(f"commitSHA: expected 'abc123def456', got '{data.get('commitSHA')}'")
    if data.get("headers.webhook-key") != "test-key":
        errors.append(f"webhook-key header: expected 'test-key', got '{data.get('webhook-key')}'")

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        sys.exit(1)

    print("All assertions passed.")


if __name__ == "__main__":
    main()
