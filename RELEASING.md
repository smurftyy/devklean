# Releasing devklean

This is the maintainer reference for cutting a release. CI and the release
workflow do the heavy lifting; your job is to bump the version, update the
changelog, and push a tag.

## Single source of truth

The version lives in exactly one place:

```
src/devklean/_version.py   ->   __version__ = "X.Y.Z"
```

Hatchling reads it (`[tool.hatch.version]` in `pyproject.toml`), so there is no
version string to update anywhere else — not in `pyproject.toml`, not in the
docs.

## Pre-flight checklist

```bash
ruff check . && ruff format --check . && mypy   # lint + types clean
pytest                                          # tests green
python -m build                                 # builds sdist + wheel
twine check dist/*                              # metadata valid
```

All four green? Proceed.

## Cutting a release

1. **Bump the version** in `src/devklean/_version.py` (follow
   [SemVer](https://semver.org/): patch for fixes, minor for features, major for
   breaking changes).
2. **Update the changelog**: move items from `## [Unreleased]` into a new
   `## [X.Y.Z] - YYYY-MM-DD` section in `CHANGELOG.md`, and refresh the compare
   links at the bottom.
3. **Commit**: `git commit -am "release: vX.Y.Z"`.
4. **Tag and push**:
   ```bash
   git tag vX.Y.Z
   git push origin main --tags
   ```

Pushing a `v*.*.*` tag triggers `.github/workflows/release.yml`, which builds the
distribution, runs `twine check`, and publishes to PyPI.

## PyPI publishing setup (one time)

The release workflow publishes via **Trusted Publishing (OIDC)** — no API token
stored in the repo. Before the first release:

1. Register the project name on PyPI (or use a pending publisher).
2. At <https://pypi.org/manage/account/publishing/>, add a trusted publisher:
   - Owner: `smurftyy`, Repository: `devklean`
   - Workflow: `release.yml`
   - Environment: `pypi`
3. Create a `pypi` environment in the repo settings (Settings → Environments).

Prefer an API token instead? Add `PYPI_API_TOKEN` under
Settings → Secrets → Actions and switch `release.yml` to the commented token
method (remove the `id-token` permission, uncomment the `password:` line).

## After releasing

- Verify the new version appears on PyPI and `pipx install devklean` works.
- Confirm the GitHub release/tag looks right.
- Open a fresh `## [Unreleased]` section in `CHANGELOG.md` for the next cycle.
