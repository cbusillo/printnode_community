# Contributing

Thank you for helping maintain this PrintNode API client. This fork aims to be careful, compatible, and easy to learn from.

## Workflow

- Open a focused pull request for every meaningful change.
- Do not commit directly to `main`.
- Keep changes small and reviewable.
- Include tests for behavior changes.
- Update documentation when user-facing behavior changes.
- Mention any command you could not run in the pull request body.

## Development

The project uses `pyproject.toml` and `uv`. Use the validation gates recorded
in `.github/github-repo-workflow.json`:

```sh
uv sync --locked
uv run pytest
uv build
uv run twine check dist/*
```

## Tests

Default tests must not require real PrintNode credentials. Use mocked HTTP responses for normal test coverage.

Live PrintNode API tests may be added, but they must be opt-in and gated by environment variables so they never run accidentally in CI or on contributor machines.

## Compatibility

Preserve the `printnode_community` import path. Breaking changes require an explicit pull request, changelog entry, and release note.

## Releases

Releases are cut only from reviewed code that has passed CI. New distribution names must be tested on TestPyPI before publishing to PyPI.
