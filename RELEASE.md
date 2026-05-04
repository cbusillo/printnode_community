# Release Process

Maintained releases are published under the `printnode_community` project name.

## Package Name

The historical PyPI distribution name is `PrintNodeApi`, but upstream has not
responded to maintainer handoff requests. This community-maintained fork
publishes as `printnode_community` instead.

PyPI normalizes `printnode-community` and `printnode_community` as the same project name. Prefer documenting `uv add printnode_community` and `python -m pip install printnode_community` so the install command visually matches the import namespace.

Before publishing from a new environment or workflow, verify the
`printnode_community` trusted publisher configuration on PyPI or TestPyPI.

## Versioning

Use semantic versioning for maintained releases.

- Patch releases: bug fixes, packaging fixes, documentation corrections, and compatibility fixes that preserve public API behavior.
- Minor releases: new PrintNode API coverage, new optional features, or deprecations that preserve compatibility.
- Major releases: breaking API changes, import-path changes, or removal of documented compatibility.

Keep the package version in `pyproject.toml` and the top `CHANGELOG.md` release section in sync.

## Pre-Release Checklist

1. Confirm PyPI/TestPyPI trusted publisher configuration is ready.
2. Confirm `main` is green in CI.
3. Create a release branch from `main`.
4. Update `pyproject.toml` with the release version.
5. Update `CHANGELOG.md` by moving relevant `Unreleased` entries under the release version and date.
6. Run local verification:

```sh
uv sync --locked
uv run pytest
rm -rf dist && uv build
uv run twine check dist/*
```

7. Open a release PR and wait for required CI checks.
8. Merge the release PR.
9. Create a signed Git tag if signing is configured; otherwise create an annotated tag:

```sh
git tag -a vX.Y.Z -m "Release vX.Y.Z"
git push origin vX.Y.Z
```

10. Optionally run the manual `Publish` workflow from the release tag for TestPyPI.
11. If TestPyPI is used, install from TestPyPI in a clean environment and smoke-test imports.
12. Run the manual `Publish` workflow from the release tag for PyPI. The workflow creates the GitHub Release from the matching `CHANGELOG.md` section after the PyPI upload succeeds.

## Optional TestPyPI Smoke Test

TestPyPI is a useful publishing dry run, but it is not required for every
release. Use a clean environment when testing a TestPyPI upload:

```sh
uv venv /tmp/printnode_community-release-smoke
source /tmp/printnode_community-release-smoke/bin/activate
uv pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ printnode_community
python -c "from printnode_community import Gateway; print(Gateway.__name__)"
deactivate
```

## GitHub Environments

Configure two GitHub environments before publishing:

- `testpypi`: no required reviewer, so TestPyPI dry runs do not pause.
- `pypi`: no GitHub environment reviewer. Production approval happens by
  merging the release PR, creating the release tag, and manually dispatching
  the publish workflow from that tag.

Configure each environment as a trusted publisher in the corresponding PyPI
project before running the workflow. TestPyPI and PyPI are separate services;
both need their own pending publisher.

Use these exact values on TestPyPI:

```text
Project name: printnode_community
Owner: cbusillo
Repository: printnode_community
Workflow: publish.yml
Environment: testpypi
```

Use these exact values on PyPI:

```text
Project name: printnode_community
Owner: cbusillo
Repository: printnode_community
Workflow: publish.yml
Environment: pypi
```

If publish fails with `invalid-publisher`, compare the claims in the failed
Actions log with the pending publisher. The expected TestPyPI claims include:

```text
sub: repo:cbusillo/printnode_community:environment:testpypi
repository: cbusillo/printnode_community
job_workflow_ref: cbusillo/printnode_community/.github/workflows/publish.yml@refs/tags/v0.3.0
ref: refs/tags/v0.3.0
```

The `Publish` workflow uses GitHub OpenID Connect through `id-token: write`; do not add PyPI API tokens unless trusted publishing is unavailable.

## Rollback

Published packages cannot be overwritten. If a bad release is published:

- yank the release on PyPI if appropriate;
- document the issue in `CHANGELOG.md` and GitHub Releases;
- publish a new patch release with the fix.
