# Repository maintenance

Canonical rules/prompts/templates are the source of truth. `skills/`, root plugin/client manifests
and `generated-distribution.json` are committed generated output for direct repository installation.
Edit sources, then run:

```text
python scripts/sync_distribution.py --write
python -m unittest discover -s scripts/tests -v
python scripts/check_repository.py
python scripts/build_release.py
```

Python 3.10+, standard library. Synchronisation owns only declared generated paths, refuses unknown
files/collisions and does no recursive deletion or Git/network operation. Builds use explicit
per-skill allowlists and LF-normalised text. Private archives, project configs, source tests and
unrelated modes are excluded. `dist/` is ignored; different existing same-version output is refused.

Use focused branches/PRs to `main`. Review source and generated diffs together. For accepted rules,
update affected guidance and fix/keep calibration while preserving IDs/provenance. See
[CONTRIBUTING.md](../CONTRIBUTING.md) and [GOVERNANCE.md](../GOVERNANCE.md).

## CI and releases

PR/branch CI runs helper/package tests on Linux/Windows with Python 3.10/3.13, checks generated
consistency/links, builds ZIPs and uploads artifacts. The aggregate status is **Required checks**.
These checks do not establish scientific validity or reliable LLM decisions; use the source
calibration cases and retain actual host/model/version when evaluating behaviour.

Update VERSION/changelog/current examples and regenerate before release. Push a `vX.Y.Z` tag
matching VERSION on the reviewed commit. The release workflow reruns checks and prepares an
unpublished release draft with ZIPs/checksums; inspect it before manual publication.

## GitHub settings

Files alone do not activate server-side protection. After the first push/check run:

1. Set `main` as default branch. Enable Actions, permit the used official `actions/*`, keep default
   token permissions read-only and require appropriate approval for outside-contributor runs.
2. Import [the branch ruleset](../.github/rulesets/main.json); require **Required checks**, code-owner
   review and resolved discussions, and block force push/deletion. Add actual reviewers with write
   access to [CODEOWNERS](../.github/CODEOWNERS). A solo maintainer needs another reviewer or an
   intentionally narrow bypass for their own PRs; the supplied ruleset has no bypass actors.
3. Prefer squash merge/head-branch deletion. Create the `release` environment with appropriate
   approval/tag restrictions and protect version tags. Available protections depend on visibility/plan.
4. Enable Issues, desired labels (`rules`, `tooling`, `documentation`, `bug`, `duplicate`,
   `skip-changelog`), optional Discussions, private vulnerability reporting and available secret protection.
5. Confirm licence/source notices and inspect the release draft before publishing. No PAT or
   automatic PR-approval setting is required by this workflow.
