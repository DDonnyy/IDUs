# Installation

Install selected skills directly:

```text
npx skills add DDonnyy/IDUs --skill idus-draft --skill idus-review --skill idus-configure --copy
```

Alternatively copy complete folders from `skills/` into the host's supported skill directory:
`.agents/skills/` for Codex or `.claude/skills/` for Claude Code. Each skill is independent; draft
needs no Python. Installer requirements and host trust/features remain client-specific.

The repository provides portable/Codex manifests and a Claude marketplace. Claude can use
`claude --plugin-dir path/to/IDUs`, or `/plugin marketplace add DDonnyy/IDUs` then
`/plugin install idus@idus` when the repository is accessible.

For release ZIPs, unpack a standalone archive into a folder matching its skill name; keep all
references/assets/notices. Plugin ZIPs start at `plugin.json`; standalone ZIPs at `SKILL.md`.

Local preferences belong in the manuscript workspace, outside the installed skill; see
[configuration.md](../configuration.md). A sole legacy config/CLI remains supported. Remove old
installed duplicate skills through the host when replacing them; installation does not delete them.

Developer builds and GitHub settings: [maintenance](repository-maintenance.md). Runtime resources
are scoped per skill and read as needed. Source tests/calibration are developer resources, not
part of installed skills. Format compatibility is separate from real-model behaviour.
