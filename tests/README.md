# Testing

The default test suite is credential-free and must not call the live PrintNode API.

Use `qualityGate.test.local` from `.github/github.json`, replacing `{test_paths}`
with affected test paths as described in [Local Verification](../AGENTS.md#local-verification).
The complete `test.ci` suite runs in CI before ready or merge.

For full package verification, follow the repository workflow metadata in
`.github/github.json`.

Live PrintNode API tests may be added later, but they must be opt-in and gated by explicit environment variables. Do not commit real API keys, account credentials, customer data, or live API fixtures.
