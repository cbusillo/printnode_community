# Changelog

All notable changes to this community-maintained fork will be documented in this file.

The format follows the spirit of Keep a Changelog, and this project intends to use semantic versioning once the first maintained release is cut.

## Unreleased

- Added repository workflow defaults for future GitHub workflow sessions.
- Added public-path coverage for model-instance computer, printer, and print
  job lookups.
- Updated post-release documentation now that `0.3.0` is published.
- Removed stale private helper code that was unreachable from account and
  computer APIs.
- Removed stale local IDE metadata and the legacy root `test` wrapper in favor
  of the documented `uv run pytest` workflow.
- Hardened model factory handling for missing or null optional nested PrintNode
  response fields.

## 0.3.0 - 2026-04-26

### Added

- Added repository governance documentation for community maintenance.
- Added contribution, security, issue, and pull request guidance.
- Added modern Python project metadata in `pyproject.toml`.
- Added an initial `uv` development workflow.
- Added release process documentation and a manual trusted-publishing workflow scaffold.
- Added `printnode_community` as the import namespace.

### Changed

- Selected `printnode_community` as the maintained project, distribution, and import name.
- Documented the plan to migrate the default branch from `master` to `main`.
- Migrated the default branch from `master` to `main`.
- Replaced legacy `setup.py` packaging with `pyproject.toml`.
- Replaced legacy live-credential test guidance with credential-free `uv` test instructions.

### Removed

- Removed stale placeholder credential and fixture files from the legacy live test setup.

### Notes

- This fork is not an official PrintNode release unless PrintNode explicitly confirms maintainership or transfer.
