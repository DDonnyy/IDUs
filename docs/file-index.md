# IDUs file index

This checkout has **162 public files**, including **72 managed generated files**.
Private outputs, source archives and project settings are excluded. This index is maintainer
documentation and is not loaded or bundled by the installed skills.

Edit canonical sources. Regenerate skills/manifests with `scripts/sync_distribution.py`.
All modes receive the same `rules.md`; draft selects its short core and needed definitions,
while review follows detailed checks. See the [skill map](skill-map.md) for transitions.

## Canonical sources and maintenance

| File | Purpose | Packaged in |
|---|---|---|
| [.editorconfig](../.editorconfig) | Editor formatting conventions. | repository only |
| [.gitattributes](../.gitattributes) | Git text and line-ending conventions. | repository only |
| [.github/CODEOWNERS](../.github/CODEOWNERS) | Repository review ownership. | repository only |
| [.github/ISSUE_TEMPLATE/bug_report.yml](../.github/ISSUE_TEMPLATE/bug_report.yml) | Structured bug report fields. | repository only |
| [.github/ISSUE_TEMPLATE/config.yml](../.github/ISSUE_TEMPLATE/config.yml) | Issue-template chooser settings. | repository only |
| [.github/ISSUE_TEMPLATE/rule_proposal.yml](../.github/ISSUE_TEMPLATE/rule_proposal.yml) | Structured writing-rule proposal fields. | repository only |
| [.github/PULL_REQUEST_TEMPLATE.md](../.github/PULL_REQUEST_TEMPLATE.md) | PR scope, source/provenance and validation checklist. | repository only |
| [.github/dependabot.yml](../.github/dependabot.yml) | Scheduled dependency-update configuration. | repository only |
| [.github/release.yml](../.github/release.yml) | Release-note grouping by labels. | repository only |
| [.github/rulesets/main.json](../.github/rulesets/main.json) | Suggested main-branch protection configuration. | repository only |
| [.github/workflows/checks.yml](../.github/workflows/checks.yml) | OS/Python test matrix, repository/build checks and required aggregate status. | repository only |
| [.github/workflows/release.yml](../.github/workflows/release.yml) | Authorised release packaging workflow. | repository only |
| [.gitignore](../.gitignore) | Private archives, outputs, settings and local development exclusions. | repository only |
| [AGENTS.md](../AGENTS.md) | Repository maintenance instructions and authorised task boundaries. | repository only |
| [ALGORITHM.md](../ALGORITHM.md) | Review routing: argument, academic readability, verification, source anchors and delivery. | R |
| [CHANGELOG.md](../CHANGELOG.md) | Versioned user-facing change history. | repository only |
| [CONTRIBUTING.md](../CONTRIBUTING.md) | Focused PRs, proposal acceptance, source edits and required checks. | repository only |
| [GOVERNANCE.md](../GOVERNANCE.md) | Maintainer decisions and how accepted guidance becomes active. | repository only |
| [LICENSE](../LICENSE) | Apache-2.0 terms for original toolkit contributions. | C / D / R |
| [NOTICE](../NOTICE) | Project attribution and source notices. | C / D / R |
| [README.md](../README.md) | Public entry points, installation and development commands. | repository only |
| [SECURITY.md](../SECURITY.md) | Sensitive-report channel and supported security reporting practices. | repository only |
| [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md) | Third-party source rights and exclusions from the distributed toolkit. | C / D / R |
| [VERSION](../VERSION) | Current distribution version; builds do not publish a release. | C / D / R |
| [checklists/draft_check.md](../checklists/draft_check.md) | Short content/coherence check for a first draft. | D |
| [checklists/final_check.md](../checklists/final_check.md) | Review completion, meaning, source mapping and application checks. | R |
| [configuration.md](../configuration.md) | Scoped project settings, USR/TERM entries, previews, revisions, backups and expert-feedback routing. | C / R |
| [contracts.md](../contracts.md) | Optional review request/report contracts and the limits of structural validation. | R |
| [contributions.md](../contributions.md) | Shared-rule assessment, semantic overlap, provenance, fix/keep cases and proposal submission. | C |
| [contributions/proposals/PROP-ACADEMIC-READABILITY.json](../contributions/proposals/PROP-ACADEMIC-READABILITY.json) | Historical accepted proposal behind the C1/C2/C8/A4 refinements; preserves its base provenance. | repository only |
| [docs/file-index.md](../docs/file-index.md) | This complete source/generated file index. | repository only |
| [docs/installation.md](../docs/installation.md) | Host-specific installation and copied-package guidance. | repository only |
| [docs/repository-maintenance.md](../docs/repository-maintenance.md) | CLI/CI maintenance, release workflow and GitHub settings. | repository only |
| [docs/skill-map.md](../docs/skill-map.md) | Instruction routes for all modes, shared rules, helpers and packaging. | repository only |
| [drafting.md](../drafting.md) | First-draft workflow; selects the shared core and needed definitions, then one content/coherence reread. | C / D |
| [evals/activation.json](../evals/activation.json) | Skill-selection scenarios and expected activation boundaries. | repository only |
| [examples/configuration/config.json](../examples/configuration/config.json) | Complete synthetic project configuration. | C |
| [examples/configuration/custom-rule.json](../examples/configuration/custom-rule.json) | Synthetic scoped USR rule entry. | C |
| [examples/configuration/custom-term.json](../examples/configuration/custom-term.json) | Synthetic contextual TERM entry. | C |
| [examples/configuration/profile.json](../examples/configuration/profile.json) | Synthetic profile patch. | C |
| [examples/contributions/proposal.json](../examples/contributions/proposal.json) | Proposal contract example with deliberately pending reviews. | C |
| [examples/draft_case.md](../examples/draft_case.md) | Synthetic notes and a bounded first-draft example. | D |
| [examples/regression_cases.md](../examples/regression_cases.md) | Manual mode/editorial calibration and fix/keep decisions; not measured model accuracy. | repository only |
| [examples/report/manuscript.txt](../examples/report/manuscript.txt) | Synthetic text snapshot for the report example. | R |
| [examples/report/report.json](../examples/report/report.json) | Review report example tied to a text snapshot. | R |
| [examples/report/request.json](../examples/report/request.json) | Optional machine-readable review request example. | R |
| [generated-distribution.json](../generated-distribution.json) | Managed generated-file paths and hashes used by synchronisation. | repository only |
| [packaging/helpers/idus-configure.md.in](../packaging/helpers/idus-configure.md.in) | Mode-specific helper guide included as scripts/README.md. | C |
| [packaging/helpers/idus-review.md.in](../packaging/helpers/idus-review.md.in) | Mode-specific helper guide included as scripts/README.md. | R |
| [packaging/release-readme.md.in](../packaging/release-readme.md.in) | README template for the standalone plugin build. | repository only |
| [packaging/skills/idus-configure/SKILL.md.in](../packaging/skills/idus-configure/SKILL.md.in) | Canonical idus-configure entry point and resource routing. | C |
| [packaging/skills/idus-draft/SKILL.md.in](../packaging/skills/idus-draft/SKILL.md.in) | Canonical idus-draft entry point and resource routing. | D |
| [packaging/skills/idus-review/SKILL.md.in](../packaging/skills/idus-review/SKILL.md.in) | Canonical idus-review entry point and resource routing. | R |
| [prompts/configure_agent.md](../prompts/configure_agent.md) | Standalone local-settings and reusable-guidance instructions. | repository only |
| [prompts/contribution_agent.md](../prompts/contribution_agent.md) | Standalone shared-rule proposal preparation instructions. | repository only |
| [prompts/draft_agent.md](../prompts/draft_agent.md) | Standalone first-draft instructions, usable without installation. | repository only |
| [prompts/editor_diff_analyst.md](../prompts/editor_diff_analyst.md) | Before/after expert-edit analysis, scope and source interpretation. | repository only |
| [prompts/main_agent.md](../prompts/main_agent.md) | Self-contained routing and safeguards for draft, review and configuration. | repository only |
| [references/README.md](../references/README.md) | Private source-archive boundary; source documents are not bundled. | repository only |
| [rules.md](../rules.md) | Single writing corpus: short core, all stable rule IDs, structure, evidence, word choice and punctuation. | C / D / R |
| [scripts/README.md](../scripts/README.md) | Developer-facing helper usage, safeguards and verification commands. | repository only |
| [scripts/apply_edits.py](../scripts/apply_edits.py) | Dry-run edit batches with unique anchors, authorised writes and recovery. | R |
| [scripts/build_release.py](../scripts/build_release.py) | Explicit public allowlist, independent packages, checksums and deterministic archives. | repository only |
| [scripts/check_repository.py](../scripts/check_repository.py) | Public Markdown links, metadata and generated-distribution consistency. | repository only |
| [scripts/cli_io.py](../scripts/cli_io.py) | Consistent UTF-8 output for redirected CLI streams. | C / R |
| [scripts/comma_candidates.py](../scripts/comma_candidates.py) | Read-only punctuation candidates requiring contextual review. | R |
| [scripts/configuration.py](../scripts/configuration.py) | Scoped settings, changes, backups, revision checks and term candidates. | C / R |
| [scripts/contributions.py](../scripts/contributions.py) | Corpus indexing, proposal checks and local sanitised packet export. | C |
| [scripts/idus.py](../scripts/idus.py) | CLI router for the helpers available in each installed mode. | C / R |
| [scripts/paperidu.py](../scripts/paperidu.py) | Legacy CLI forwarding alias. | C / R |
| [scripts/review_report.py](../scripts/review_report.py) | Review contract checks, supplied snapshot quotations and report rendering. | R |
| [scripts/schema_validation.py](../scripts/schema_validation.py) | Standard-library JSON contract validation. | C / R |
| [scripts/schemas/config.schema.json](../scripts/schemas/config.schema.json) | IDUs project configuration v1. | C / R |
| [scripts/schemas/proposal.schema.json](../scripts/schemas/proposal.schema.json) | IDUs shared-rule proposal, not an accepted rule. | C |
| [scripts/schemas/report.schema.json](../scripts/schemas/report.schema.json) | IDUs review report v1. | R |
| [scripts/schemas/request.schema.json](../scripts/schemas/request.schema.json) | IDUs review request v1. | R |
| [scripts/spelling_pass.py](../scripts/spelling_pass.py) | Read-only spelling candidates for the selected variety. | R |
| [scripts/sync_distribution.py](../scripts/sync_distribution.py) | Refresh or check only owned generated skills/manifests. | repository only |
| [scripts/tests/test_cli_unicode.py](../scripts/tests/test_cli_unicode.py) | Redirected Unicode CLI handling, including legacy code pages. | repository only |
| [scripts/tests/test_configuration.py](../scripts/tests/test_configuration.py) | Settings scope, updates, conflicts, revisions, backups and candidate scanning. | repository only |
| [scripts/tests/test_contracts.py](../scripts/tests/test_contracts.py) | Request/report structure, evidence states and supplied quotation checks. | repository only |
| [scripts/tests/test_contributions.py](../scripts/tests/test_contributions.py) | Proposal transport, overlap declarations, export/privacy guards and fingerprints. | repository only |
| [scripts/tests/test_distribution_sync.py](../scripts/tests/test_distribution_sync.py) | Generated ownership, stale output, idempotence and private-output exclusions. | repository only |
| [scripts/tests/test_release.py](../scripts/tests/test_release.py) | Independent packages, shared corpus equality, public boundaries and reproducibility. | repository only |
| [scripts/tests/test_scripts.py](../scripts/tests/test_scripts.py) | Edit application, path safety, recovery and read-only scanner behaviour. | repository only |
| [sources.md](../sources.md) | Source families, provenance, public/private boundaries and limits of generalisation. | C / D / R |
| [templates/draft_brief.md](../templates/draft_brief.md) | Optional intake format for research notes and a drafting request. | D |
| [templates/draft_delivery.md](../templates/draft_delivery.md) | Draft output with source mapping, gaps and short author notes. | D |
| [templates/paper_profile.md](../templates/paper_profile.md) | Optional manuscript context, evidence, style and permission notes. | R |
| [templates/review_report.md](../templates/review_report.md) | Located findings with separate wording, evidence and application status. | R |

D = draft, R = review, C = configure. Repository-only files support maintenance or direct
use; they are not copied into installed skills.

## Generated copies

| File | Canonical source | Purpose |
|---|---|---|
| [.claude-plugin/marketplace.json](../.claude-plugin/marketplace.json) | [scripts/build_release.py](../scripts/build_release.py) | Generated plugin/marketplace metadata. |
| [.claude-plugin/plugin.json](../.claude-plugin/plugin.json) | [scripts/build_release.py](../scripts/build_release.py) | Generated plugin/marketplace metadata. |
| [.codex-plugin/plugin.json](../.codex-plugin/plugin.json) | [scripts/build_release.py](../scripts/build_release.py) | Generated plugin/marketplace metadata. |
| [plugin.json](../plugin.json) | [scripts/build_release.py](../scripts/build_release.py) | Generated plugin/marketplace metadata. |
| [skills/idus-configure/LICENSE](../skills/idus-configure/LICENSE) | [LICENSE](../LICENSE) | Apache-2.0 terms for original toolkit contributions. |
| [skills/idus-configure/NOTICE](../skills/idus-configure/NOTICE) | [NOTICE](../NOTICE) | Project attribution and source notices. |
| [skills/idus-configure/SKILL.md](../skills/idus-configure/SKILL.md) | [packaging/skills/idus-configure/SKILL.md.in](../packaging/skills/idus-configure/SKILL.md.in) | Canonical idus-configure entry point and resource routing. |
| [skills/idus-configure/THIRD_PARTY_NOTICES.md](../skills/idus-configure/THIRD_PARTY_NOTICES.md) | [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md) | Third-party source rights and exclusions from the distributed toolkit. |
| [skills/idus-configure/VERSION](../skills/idus-configure/VERSION) | [VERSION](../VERSION) | Distribution version. |
| [skills/idus-configure/checksums.json](../skills/idus-configure/checksums.json) | [scripts/build_release.py](../scripts/build_release.py) | Hashes of the independent package contents. |
| [skills/idus-configure/examples/configuration/config.json](../skills/idus-configure/examples/configuration/config.json) | [examples/configuration/config.json](../examples/configuration/config.json) | Complete synthetic project configuration. |
| [skills/idus-configure/examples/configuration/custom-rule.json](../skills/idus-configure/examples/configuration/custom-rule.json) | [examples/configuration/custom-rule.json](../examples/configuration/custom-rule.json) | Synthetic scoped USR rule entry. |
| [skills/idus-configure/examples/configuration/custom-term.json](../skills/idus-configure/examples/configuration/custom-term.json) | [examples/configuration/custom-term.json](../examples/configuration/custom-term.json) | Synthetic contextual TERM entry. |
| [skills/idus-configure/examples/configuration/profile.json](../skills/idus-configure/examples/configuration/profile.json) | [examples/configuration/profile.json](../examples/configuration/profile.json) | Synthetic profile patch. |
| [skills/idus-configure/examples/contributions/proposal.json](../skills/idus-configure/examples/contributions/proposal.json) | [examples/contributions/proposal.json](../examples/contributions/proposal.json) | Proposal contract example with deliberately pending reviews. |
| [skills/idus-configure/references/configuration.md](../skills/idus-configure/references/configuration.md) | [configuration.md](../configuration.md) | Scoped project settings, USR/TERM entries, previews, revisions, backups and expert-feedback routing. |
| [skills/idus-configure/references/contributions.md](../skills/idus-configure/references/contributions.md) | [contributions.md](../contributions.md) | Shared-rule assessment, semantic overlap, provenance, fix/keep cases and proposal submission. |
| [skills/idus-configure/references/drafting.md](../skills/idus-configure/references/drafting.md) | [drafting.md](../drafting.md) | First-draft workflow; selects the shared core and needed definitions, then one content/coherence reread. |
| [skills/idus-configure/references/rules.md](../skills/idus-configure/references/rules.md) | [rules.md](../rules.md) | Single writing corpus: short core, all stable rule IDs, structure, evidence, word choice and punctuation. |
| [skills/idus-configure/references/sources.md](../skills/idus-configure/references/sources.md) | [sources.md](../sources.md) | Source families, provenance, public/private boundaries and limits of generalisation. |
| [skills/idus-configure/scripts/README.md](../skills/idus-configure/scripts/README.md) | [packaging/helpers/idus-configure.md.in](../packaging/helpers/idus-configure.md.in) | Mode-specific helper guide included as scripts/README.md. |
| [skills/idus-configure/scripts/cli_io.py](../skills/idus-configure/scripts/cli_io.py) | [scripts/cli_io.py](../scripts/cli_io.py) | Consistent UTF-8 output for redirected CLI streams. |
| [skills/idus-configure/scripts/configuration.py](../skills/idus-configure/scripts/configuration.py) | [scripts/configuration.py](../scripts/configuration.py) | Scoped settings, changes, backups, revision checks and term candidates. |
| [skills/idus-configure/scripts/contributions.py](../skills/idus-configure/scripts/contributions.py) | [scripts/contributions.py](../scripts/contributions.py) | Corpus indexing, proposal checks and local sanitised packet export. |
| [skills/idus-configure/scripts/idus.py](../skills/idus-configure/scripts/idus.py) | [scripts/idus.py](../scripts/idus.py) | CLI router for the helpers available in each installed mode. |
| [skills/idus-configure/scripts/paperidu.py](../skills/idus-configure/scripts/paperidu.py) | [scripts/paperidu.py](../scripts/paperidu.py) | Legacy CLI forwarding alias. |
| [skills/idus-configure/scripts/schema_validation.py](../skills/idus-configure/scripts/schema_validation.py) | [scripts/schema_validation.py](../scripts/schema_validation.py) | Standard-library JSON contract validation. |
| [skills/idus-configure/scripts/schemas/config.schema.json](../skills/idus-configure/scripts/schemas/config.schema.json) | [scripts/schemas/config.schema.json](../scripts/schemas/config.schema.json) | IDUs project configuration v1. |
| [skills/idus-configure/scripts/schemas/proposal.schema.json](../skills/idus-configure/scripts/schemas/proposal.schema.json) | [scripts/schemas/proposal.schema.json](../scripts/schemas/proposal.schema.json) | IDUs shared-rule proposal, not an accepted rule. |
| [skills/idus-draft/LICENSE](../skills/idus-draft/LICENSE) | [LICENSE](../LICENSE) | Apache-2.0 terms for original toolkit contributions. |
| [skills/idus-draft/NOTICE](../skills/idus-draft/NOTICE) | [NOTICE](../NOTICE) | Project attribution and source notices. |
| [skills/idus-draft/SKILL.md](../skills/idus-draft/SKILL.md) | [packaging/skills/idus-draft/SKILL.md.in](../packaging/skills/idus-draft/SKILL.md.in) | Canonical idus-draft entry point and resource routing. |
| [skills/idus-draft/THIRD_PARTY_NOTICES.md](../skills/idus-draft/THIRD_PARTY_NOTICES.md) | [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md) | Third-party source rights and exclusions from the distributed toolkit. |
| [skills/idus-draft/VERSION](../skills/idus-draft/VERSION) | [VERSION](../VERSION) | Distribution version. |
| [skills/idus-draft/assets/templates/draft_brief.md](../skills/idus-draft/assets/templates/draft_brief.md) | [templates/draft_brief.md](../templates/draft_brief.md) | Optional intake format for research notes and a drafting request. |
| [skills/idus-draft/assets/templates/draft_delivery.md](../skills/idus-draft/assets/templates/draft_delivery.md) | [templates/draft_delivery.md](../templates/draft_delivery.md) | Draft output with source mapping, gaps and short author notes. |
| [skills/idus-draft/checksums.json](../skills/idus-draft/checksums.json) | [scripts/build_release.py](../scripts/build_release.py) | Hashes of the independent package contents. |
| [skills/idus-draft/references/checklists/draft_check.md](../skills/idus-draft/references/checklists/draft_check.md) | [checklists/draft_check.md](../checklists/draft_check.md) | Short content/coherence check for a first draft. |
| [skills/idus-draft/references/drafting.md](../skills/idus-draft/references/drafting.md) | [drafting.md](../drafting.md) | First-draft workflow; selects the shared core and needed definitions, then one content/coherence reread. |
| [skills/idus-draft/references/examples/draft_case.md](../skills/idus-draft/references/examples/draft_case.md) | [examples/draft_case.md](../examples/draft_case.md) | Synthetic notes and a bounded first-draft example. |
| [skills/idus-draft/references/rules.md](../skills/idus-draft/references/rules.md) | [rules.md](../rules.md) | Single writing corpus: short core, all stable rule IDs, structure, evidence, word choice and punctuation. |
| [skills/idus-draft/references/sources.md](../skills/idus-draft/references/sources.md) | [sources.md](../sources.md) | Source families, provenance, public/private boundaries and limits of generalisation. |
| [skills/idus-review/LICENSE](../skills/idus-review/LICENSE) | [LICENSE](../LICENSE) | Apache-2.0 terms for original toolkit contributions. |
| [skills/idus-review/NOTICE](../skills/idus-review/NOTICE) | [NOTICE](../NOTICE) | Project attribution and source notices. |
| [skills/idus-review/SKILL.md](../skills/idus-review/SKILL.md) | [packaging/skills/idus-review/SKILL.md.in](../packaging/skills/idus-review/SKILL.md.in) | Canonical idus-review entry point and resource routing. |
| [skills/idus-review/THIRD_PARTY_NOTICES.md](../skills/idus-review/THIRD_PARTY_NOTICES.md) | [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md) | Third-party source rights and exclusions from the distributed toolkit. |
| [skills/idus-review/VERSION](../skills/idus-review/VERSION) | [VERSION](../VERSION) | Distribution version. |
| [skills/idus-review/assets/templates/paper_profile.md](../skills/idus-review/assets/templates/paper_profile.md) | [templates/paper_profile.md](../templates/paper_profile.md) | Optional manuscript context, evidence, style and permission notes. |
| [skills/idus-review/assets/templates/review_report.md](../skills/idus-review/assets/templates/review_report.md) | [templates/review_report.md](../templates/review_report.md) | Located findings with separate wording, evidence and application status. |
| [skills/idus-review/checksums.json](../skills/idus-review/checksums.json) | [scripts/build_release.py](../scripts/build_release.py) | Hashes of the independent package contents. |
| [skills/idus-review/examples/report/manuscript.txt](../skills/idus-review/examples/report/manuscript.txt) | [examples/report/manuscript.txt](../examples/report/manuscript.txt) | Synthetic text snapshot for the report example. |
| [skills/idus-review/examples/report/report.json](../skills/idus-review/examples/report/report.json) | [examples/report/report.json](../examples/report/report.json) | Review report example tied to a text snapshot. |
| [skills/idus-review/examples/report/request.json](../skills/idus-review/examples/report/request.json) | [examples/report/request.json](../examples/report/request.json) | Optional machine-readable review request example. |
| [skills/idus-review/references/ALGORITHM.md](../skills/idus-review/references/ALGORITHM.md) | [ALGORITHM.md](../ALGORITHM.md) | Review routing: argument, academic readability, verification, source anchors and delivery. |
| [skills/idus-review/references/checklists/final_check.md](../skills/idus-review/references/checklists/final_check.md) | [checklists/final_check.md](../checklists/final_check.md) | Review completion, meaning, source mapping and application checks. |
| [skills/idus-review/references/configuration.md](../skills/idus-review/references/configuration.md) | [configuration.md](../configuration.md) | Scoped project settings, USR/TERM entries, previews, revisions, backups and expert-feedback routing. |
| [skills/idus-review/references/contracts.md](../skills/idus-review/references/contracts.md) | [contracts.md](../contracts.md) | Optional review request/report contracts and the limits of structural validation. |
| [skills/idus-review/references/rules.md](../skills/idus-review/references/rules.md) | [rules.md](../rules.md) | Single writing corpus: short core, all stable rule IDs, structure, evidence, word choice and punctuation. |
| [skills/idus-review/references/sources.md](../skills/idus-review/references/sources.md) | [sources.md](../sources.md) | Source families, provenance, public/private boundaries and limits of generalisation. |
| [skills/idus-review/scripts/README.md](../skills/idus-review/scripts/README.md) | [packaging/helpers/idus-review.md.in](../packaging/helpers/idus-review.md.in) | Mode-specific helper guide included as scripts/README.md. |
| [skills/idus-review/scripts/apply_edits.py](../skills/idus-review/scripts/apply_edits.py) | [scripts/apply_edits.py](../scripts/apply_edits.py) | Dry-run edit batches with unique anchors, authorised writes and recovery. |
| [skills/idus-review/scripts/cli_io.py](../skills/idus-review/scripts/cli_io.py) | [scripts/cli_io.py](../scripts/cli_io.py) | Consistent UTF-8 output for redirected CLI streams. |
| [skills/idus-review/scripts/comma_candidates.py](../skills/idus-review/scripts/comma_candidates.py) | [scripts/comma_candidates.py](../scripts/comma_candidates.py) | Read-only punctuation candidates requiring contextual review. |
| [skills/idus-review/scripts/configuration.py](../skills/idus-review/scripts/configuration.py) | [scripts/configuration.py](../scripts/configuration.py) | Scoped settings, changes, backups, revision checks and term candidates. |
| [skills/idus-review/scripts/idus.py](../skills/idus-review/scripts/idus.py) | [scripts/idus.py](../scripts/idus.py) | CLI router for the helpers available in each installed mode. |
| [skills/idus-review/scripts/paperidu.py](../skills/idus-review/scripts/paperidu.py) | [scripts/paperidu.py](../scripts/paperidu.py) | Legacy CLI forwarding alias. |
| [skills/idus-review/scripts/review_report.py](../skills/idus-review/scripts/review_report.py) | [scripts/review_report.py](../scripts/review_report.py) | Review contract checks, supplied snapshot quotations and report rendering. |
| [skills/idus-review/scripts/schema_validation.py](../skills/idus-review/scripts/schema_validation.py) | [scripts/schema_validation.py](../scripts/schema_validation.py) | Standard-library JSON contract validation. |
| [skills/idus-review/scripts/schemas/config.schema.json](../skills/idus-review/scripts/schemas/config.schema.json) | [scripts/schemas/config.schema.json](../scripts/schemas/config.schema.json) | IDUs project configuration v1. |
| [skills/idus-review/scripts/schemas/report.schema.json](../skills/idus-review/scripts/schemas/report.schema.json) | [scripts/schemas/report.schema.json](../scripts/schemas/report.schema.json) | IDUs review report v1. |
| [skills/idus-review/scripts/schemas/request.schema.json](../skills/idus-review/scripts/schemas/request.schema.json) | [scripts/schemas/request.schema.json](../scripts/schemas/request.schema.json) | IDUs review request v1. |
| [skills/idus-review/scripts/spelling_pass.py](../skills/idus-review/scripts/spelling_pass.py) | [scripts/spelling_pass.py](../scripts/spelling_pass.py) | Read-only spelling candidates for the selected variety. |
