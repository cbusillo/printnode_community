# Contributing

Thank you for helping maintain this PrintNode API client. This fork aims to be careful, compatible, and easy to learn from.

## Workflow

Follow [repository direction](AGENTS.md#direction) and [Branch and PR Rules](AGENTS.md#branch-and-pr-rules).

- Include tests for behavior changes.
- Update documentation when user-facing behavior changes.
- Mention any command you could not run in the pull request body.

## Development

The project uses `pyproject.toml` and `uv`. Use the validation gates recorded
in `.github/github.json`:

```sh
uv sync --locked
uv build
uv run twine check dist/*
```

Select local tests under [Local Verification](AGENTS.md#local-verification).

## Tests

Follow [Testing Standards](AGENTS.md#testing-standards).

## Compatibility

Preserve the `printnode_community` import path. Breaking changes require an explicit pull request, changelog entry, and release note.

## Releases

Releases are cut only from reviewed code that has passed CI. Prefer TestPyPI
before first publishing under a new distribution name. It may
be skipped when CI, build metadata checks, and release-tag guards are sufficient;
see [RELEASE.md](RELEASE.md).
