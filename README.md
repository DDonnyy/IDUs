# IDUs — IDU-scientist

Agent Skills for English scientific writing, manuscript review and expert-derived community rules.

```text
npx skills add DDonnyy/IDUs --skill idus-draft --skill idus-review --skill idus-configure --copy
```

Install only the skills you need. Each is self-contained; Python is optional for review/configuration
helpers and unnecessary for draft. See [installation](docs/installation.md) for copied skills/plugins.

| Skill | Request | Output |
|---|---|---|
| `idus-draft` | First version from research notes, findings or rough prose | English draft, specific gap markers and short author notes |
| `idus-review` | Audit or authorised edits of existing prose | Located findings, evidence/wording verdicts and a diff where applicable |
| `idus-configure` | Project settings or reusable guidance from expert edits | Scoped rules/terms or a sanitised contribution proposal |

For example: “Use idus-draft. Draft Methods from these notes; keep missing details as TODOs.”
For direct use without installation, copy [the standalone prompt](prompts/main_agent.md), or use
[the draft prompt](prompts/draft_agent.md) / [configure prompt](prompts/configure_agent.md).

The author supplies research and intended claims. Preserve uncertainty, defined terms, numbers and
conditions; missing support stays explicit. Clear wording can remain unchanged. Style preferences
are scoped, and an expert edit is evidence to assess rather than a universal rule.

Project settings live in `.idus/config.json` in the manuscript workspace. Shared-rule preparation
checks semantic overlap, provenance and fix/keep examples; maintainers decide acceptance.
See [settings](configuration.md), [contributions](contributions.md) and [source provenance](sources.md).

## Contribute and develop

Edit canonical sources, not generated `skills/`, then run:

```text
python scripts/sync_distribution.py --write
python -m unittest discover -s scripts/tests -v
python scripts/check_repository.py
python scripts/build_release.py
```

Python 3.10+, standard library. [CONTRIBUTING.md](CONTRIBUTING.md) covers PRs;
[maintenance](docs/repository-maintenance.md) covers CI, releases and GitHub settings.
Tests check helper/packaging behaviour, not scientific validity or model reliability.

Apache-2.0 for original toolkit contributions: [LICENSE](LICENSE), [NOTICE](NOTICE),
[third-party rights](THIRD_PARTY_NOTICES.md). Private reference archives are not distributed.
