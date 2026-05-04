# Testing

The default test suite is credential-free and must not call the live PrintNode API.

Run tests with the gate recorded in `.github/github-repo-workflow.json`:

```sh
uv run pytest
```

For full package verification, follow the repository workflow metadata in
`.github/github-repo-workflow.json`.

Live PrintNode API tests may be added later, but they must be opt-in and gated by explicit environment variables. Do not commit real API keys, account credentials, customer data, or live API fixtures.
