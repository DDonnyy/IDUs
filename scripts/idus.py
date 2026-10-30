"""IDUs configuration, candidate scanning and report utilities. No model or server required."""

import argparse
import json
import sys
from pathlib import Path

import configuration
from cli_io import configure_utf8_output
from schema_validation import ContractError, read_json


def parser():
    root = argparse.ArgumentParser(description=__doc__)
    root.add_argument(
        "--version",
        action="version",
        version=(Path(__file__).resolve().parent.parent / "VERSION").read_text(encoding="utf-8").strip(),
    )
    commands = root.add_subparsers(dest="command", required=True)
    config = commands.add_parser("config", help="project-local profiles, custom rules and lexicon")
    actions = config.add_subparsers(dest="action", required=True)
    for action in [
        "show",
        "validate",
        "init",
        "set-profile",
        "import",
        "add-rule",
        "update-rule",
        "remove-rule",
        "add-term",
        "update-term",
        "remove-term",
    ]:
        item = actions.add_parser(action)
        item.add_argument("workspace", type=Path)
        if action in {"set-profile", "import", "add-rule", "update-rule", "add-term", "update-term"}:
            item.add_argument("input", type=Path, help="JSON patch, configuration, or single custom entry")
        elif action.startswith("remove"):
            item.add_argument("identifier")
        if action not in {"show", "validate"}:
            item.add_argument("--apply", action="store_true", help="persist the previewed change")
    scan = commands.add_parser("scan-terms", help="list candidates from the active project lexicon")
    scan.add_argument("workspace", type=Path)
    scan.add_argument("files", type=Path, nargs="+")
    if Path(__file__).with_name("review_report.py").is_file():
        request = commands.add_parser("validate-request")
        request.add_argument("input", type=Path)
        report = commands.add_parser("validate-report")
        report.add_argument("input", type=Path)
        report.add_argument("--snapshot", action="append", default=[], metavar="DOCUMENT_ID=FILE")
        report.add_argument(
            "--markdown", type=Path, help="write a new Markdown report; existing files are preserved"
        )
    if Path(__file__).with_name("contributions.py").is_file():
        proposal = commands.add_parser("proposal", help="local shared-rule proposals; never sends a PR")
        proposal_actions = proposal.add_subparsers(dest="action", required=True)
        for action in ["check", "overlaps", "export"]:
            item = proposal_actions.add_parser(action)
            item.add_argument(
                "input", type=Path, help="proposal JSON, not a manuscript or full configuration"
            )
            if action == "check":
                item.add_argument(
                    "--ready", action="store_true", help="also require current overlap and sharing reviews"
                )
            if action == "export":
                item.add_argument(
                    "output", type=Path, help="new local directory for the shareable proposal and PR body"
                )
    return root


def run(args):
    if args.command == "config":
        if args.action in {"show", "validate"}:
            target, original, config = configuration.load_config(args.workspace)
            if args.action == "show":
                print(json.dumps(config, ensure_ascii=False, indent=2))
            else:
                print(
                    f"Valid configuration at {target}"
                    if original is not None
                    else "No project file; built-in defaults apply."
                )
            return
        value = read_json(args.input) if hasattr(args, "input") else None
        target, original, proposed = configuration.prepare_change(
            args.workspace, args.action, value, getattr(args, "identifier", None)
        )
        difference = configuration.change_diff(target, original, proposed)
        print(difference or "No changes.")
        if args.apply:
            backup = configuration.apply_change(args.workspace, target, original, proposed)
            print(f"Configuration saved: {target}")
            if backup is not None:
                print(f"Previous configuration: {backup}")
        else:
            print("Dry run: no files changed. Use --apply within the user's existing authorisation.")
    elif args.command == "scan-terms":
        print(json.dumps(configuration.scan_terms(args.workspace, args.files), ensure_ascii=False, indent=2))
    elif args.command == "proposal":
        import contributions

        proposal = read_json(args.input)
        if args.action == "overlaps":
            result = contributions.overlap_candidates(proposal)
        elif args.action == "export":
            result = contributions.export_proposal(proposal, args.output)
        else:
            result = contributions.validate_proposal(proposal, ready=args.ready)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.command == "validate-request":
        from review_report import validate_request

        validate_request(read_json(args.input))
        print("Valid review request (paths and contents were not opened).")
    elif args.command == "validate-report":
        from review_report import render_markdown, validate_report

        report = read_json(args.input)
        snapshots = {}
        for value in args.snapshot:
            identifier, separator, filename = value.partition("=")
            if not separator or not filename or identifier in snapshots:
                raise ContractError("use one --snapshot DOCUMENT_ID=FILE per document")
            snapshots[identifier] = Path(filename)
        result = validate_report(report, snapshots)
        if args.markdown is not None:
            # A report path is explicitly provided by the caller. Never overwrite a manuscript.
            with args.markdown.open("x", encoding="utf-8", newline="\n") as stream:
                stream.write(render_markdown(report))
        print(json.dumps(result, ensure_ascii=False, indent=2))


def main():
    configure_utf8_output()
    try:
        run(parser().parse_args())
    except (OSError, ValueError, UnicodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
