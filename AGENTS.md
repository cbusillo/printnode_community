# AGENTS.md

## What PrintNode Community does

PrintNode Community is a community-maintained Python client for the PrintNode remote-printing API.
It lets Python programs call PrintNode's printing services; it is not an official PrintNode release.
Evidence: [README.md](README.md).

## Project Mission

Prioritize correctness, compatibility, clear releases, and a learning-friendly development workflow.

## Branch and PR Rules

- The default branch is `main`.
- Keep repo workflow defaults in `.github/github.json` so future
  GitHub workflow sessions can discover non-secret repo workflow facts,
  validation commands, GitHub signal availability, docs routing, important
  workflows, and cleanup policy.
- Do not commit directly to `main`.
- Use a focused branch and pull request for every meaningful change.
- Keep pull requests small enough to review.
- Require tests and CI before merge whenever the change affects code, packaging, or release behavior.
- Treat default-branch migration and repository settings as explicit maintenance tasks.
- Follow the Director's [overall direction](https://github.com/cbusillo/direction/blob/HEAD/DIRECTION.md)
  for ordinary engineering within the authorized task, including task-branch
  pushes and pull requests. Apply its Stop Boundaries; task-specific action
  limits still apply. Merge only when the task authorizes the change and
  destination and required checks pass.

## Python Project Standards

- Use `pyproject.toml` as the project source of truth.
- Use `uv` for local development, dependency locking, testing, and builds.
- Keep `uv.lock` committed for reproducible development and CI.
- Preserve the `printnode_community` import path unless a breaking-change pull request explicitly changes it.
- Prefer modern Python packaging practices while avoiding unnecessary rewrites.
- Write Python and Odoo JavaScript in the shared
  [Python and Odoo style](https://github.com/cbusillo/codex-skills/blob/HEAD/skills/references/python-odoo-style.md).
- This library's supported Python range in `pyproject.toml` and public API
  compatibility take precedence over Odoo runtime targets and newer typing features.

## Dependency Maintenance

- Renovate updates dependencies through `renovate.json`, which extends the shared preset.
- Renovate pull requests must pass the same CI as human pull requests.

## Testing Standards

- The default test suite must not require real PrintNode credentials.
- Use mocked HTTP tests for normal CI.
- Gate live PrintNode API tests behind explicit environment variables.
- Add or update tests for behavior changes.
- Do not remove coverage just because legacy tests are awkward.
- A test stays only if it fails when the product is broken and passes when
  someone makes an intended change.
- No test may assert a literal defined elsewhere (package version, Python or
  toolchain versions, hashes, classifiers); read it from the one source of
  truth or do not test it.
- No test may assert workflow or config text. Enforce such rules where they
  execute (the workflow itself, or a helper script with its own unit test).
- Verification code must not depend on working-tree state; check live state
  only on the path that acts on it.

## Release Standards

- Do not publish releases from unreviewed local state.
- Build and validate distributions before release.
- Prefer TestPyPI before first publishing under a new distribution name, but allow skipping it when CI, build metadata checks, and release-tag guards are sufficient.
- Run the manual `Publish` workflow from a `v*` release tag only.
- Keep the `testpypi` environment unblocked by manual review.
- Do not require GitHub environment review for `pypi`.
- Release timing follows the release rule in the Director's
  [overall direction](https://github.com/cbusillo/direction/blob/HEAD/DIRECTION.md).
- Trusted publishers must match project `printnode_community`, owner `cbusillo`, repository `printnode_community`, workflow `publish.yml`, and environment `testpypi` or `pypi`.
- Update `CHANGELOG.md` for user-visible changes.
- Keep release notes clear about whether this is an official PrintNode release or a community-maintained fork.
- Preserve `printnode_community` as the import package.

## Local Verification

Use the canonical gates from `.github/github.json`:

```sh
uv sync --locked
uv build
uv run twine check dist/*
```

For tests, follow the [local/CI command contract](https://github.com/cbusillo/codex-skills/blob/HEAD/skills/github/references/config-schema.md#workflow-metadata).
Replace `{test_paths}` in `test.local` with a nonempty selection of affected
test paths. Select complete safety modules by the changed authentication flow
or mutating endpoint and its callers. CI runs the complete `test.ci` suite
before ready or merge. Release packaging verification keeps its existing
build checks; its full-suite coverage comes from CI and Publish.

If a command cannot be run locally, mention why in the pull request body.
