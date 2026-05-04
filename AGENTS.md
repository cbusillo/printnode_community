# AGENTS.md

## Project Mission

This repository is maintained as a careful, community-oriented Python client for the PrintNode API. Prioritize correctness, compatibility, clear releases, and a learning-friendly development workflow.

## Branch and PR Rules

- The default branch is `main`.
- Keep repo workflow defaults in `.github/github-repo-workflow.json` so future
  GitHub workflow sessions can discover non-secret repo workflow facts,
  validation commands, GitHub signal availability, docs routing, important
  workflows, and cleanup policy.
- Do not commit directly to `main`.
- Use a focused branch and pull request for every meaningful change.
- Keep pull requests small enough to review.
- Require tests and CI before merge whenever the change affects code, packaging, or release behavior.
- Treat default-branch migration and repository settings as explicit maintenance tasks.
- Do not push branches or open pull requests unless the user explicitly asks for that action.

## Python Project Standards

- Use `pyproject.toml` as the project source of truth.
- Use `uv` for local development, dependency locking, testing, and builds.
- Keep `uv.lock` committed for reproducible development and CI.
- Preserve the `printnode_community` import path unless a breaking-change pull request explicitly changes it.
- Prefer modern Python packaging practices while avoiding unnecessary rewrites.

## Dependency Maintenance

- Keep Dependabot enabled for every dependency surface in the repository.
- Configure Dependabot for `uv`, GitHub Actions, and `pre-commit` when pre-commit hooks exist.
- Add new Dependabot ecosystems when new manifests are introduced.
- Dependabot pull requests must pass the same CI as human pull requests.

## Testing Standards

- The default test suite must not require real PrintNode credentials.
- Use mocked HTTP tests for normal CI.
- Gate live PrintNode API tests behind explicit environment variables.
- Add or update tests for behavior changes.
- Do not remove coverage just because legacy tests are awkward.

## Release Standards

- Do not publish releases from unreviewed local state.
- Build and validate distributions before release.
- Prefer TestPyPI before first publishing under a new distribution name, but allow skipping it when CI, build metadata checks, and release-tag guards are sufficient.
- Run the manual `Publish` workflow from a `v*` release tag only.
- Keep the `testpypi` environment unblocked by manual review.
- Do not require GitHub environment review for `pypi`; treat release PR merge,
  tag creation, and manual workflow dispatch as the publish approval path.
- Trusted publishers must match project `printnode_community`, owner `cbusillo`, repository `printnode_community`, workflow `publish.yml`, and environment `testpypi` or `pypi`.
- Update `CHANGELOG.md` for user-visible changes.
- Keep release notes clear about whether this is an official PrintNode release or a community-maintained fork.
- Preserve `printnode_community` as the import package.

## Local Verification

Use the canonical gates from `.github/github-repo-workflow.json`:

```sh
uv sync --locked
uv run pytest
uv build
uv run twine check dist/*
```

If a command cannot be run locally, mention why in the pull request body.
