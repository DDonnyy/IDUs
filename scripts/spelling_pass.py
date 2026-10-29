"""List possible American -> British (Oxford form) spelling/style changes.

    python spelling_pass.py <file> [...] [--stop-at MARKER] [--py-literals-only]

Read-only: never rewrites files. Use only if the paper profile selects this variety.
Every candidate requires contextual review: e.g. licenses may be a verb and meter
may be an instrument. Prefer an exported prose file. This is not a prose, Python,
LaTeX or reference parser: it can flag code, titles and proper names and miss valid
prose. The lowercase patterns are deliberately limited, not a complete spellcheck.

Simple masks hide single-line backticks, URLs, underscore names and PROTECTED
phrases. --stop-at skips the matching line and everything following it.
--py-literals-only is only a line-prefix filter for double-quoted strings; it does
not establish that the string is prose or protect identifiers inside that string.
"""
import argparse
import re
from pathlib import Path

#: Oxford spelling: British forms, but -ize and -yse (analyse) as the OED and OUP write them.
RULES = [
    (r"\banalyz(e|ed|es|ing)\b", r"analys\1"),
    (r"\bcolor(s|ed|ing)?\b", r"colour\1"),
    (r"\bcenter(s|line)?\b", r"centre\1"),
    (r"\bcenter(ed|ing)\b", lambda m: "centr" + m.group(1)),
    (r"\b(kilo|centi|milli)?meters\b", r"\1metres"),
    (r"\b(kilo|centi|milli)?meter\b", r"\1metre"),
    (r"\bmodel(ed|ing)\b", lambda m: "modell" + m.group(1)),
    (r"\blabel(ed|ing)\b", lambda m: "labell" + m.group(1)),
    (r"\btravel(ed|ing|er|ers)\b", lambda m: "travell" + m.group(1)),
    (r"\bneighbor(s|hood|hoods|ing)?\b", r"neighbour\1"),
    (r"\bcatalog(s)?\b", r"catalogue\1"),
    (r"\bgray\b", "grey"),
    (r"\btoward\b", "towards"),  # downward, upward and forward stay: they are adjectives too
    (r"\bpercent\b", "per cent"),
    (r"\bbehavior(s|al)?\b", r"behaviour\1"),
    (r"\bfavor(s|ed|able)?\b", r"favour\1"),
    (r"\bdefense\b", "defence"),
    (r"\baging\b", "ageing"),
    (r"\blicenses\b", "licences"),  # the noun; check each hit: the verb stays "licenses"
    (r"\b(minim|maxim|summar|penal|normal|organ|recogn|real|character|priorit|optim)is(e|ed|es|ing|ation)\b",
     r"\1iz\2"),
]
PROTECTED = ["Open Database License", "General Transit Feed Specification", "transit desert", "Transit Feed"]


def protect(line: str) -> tuple[str, dict[str, str]]:
    saved: dict[str, str] = {}

    def keep(m: re.Match) -> str:
        key = f"\x00{len(saved)}\x00"
        saved[key] = m.group(0)
        return key

    pattern = "|".join([r"`[^`]*`", r"https?://\S+", r"\b\w+_\w+\b"] + [re.escape(p) for p in PROTECTED])
    return re.sub(pattern, keep, line, flags=re.I), saved


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("files", nargs="+", type=Path)
    parser.add_argument("--stop-at", default=None)
    parser.add_argument("--py-literals-only", action="store_true")
    args = parser.parse_args()

    print("Candidate scan only: check the paper profile and every context; no files are written.")
    for path in args.files:
        lines = path.read_text(encoding="utf-8").split("\n")
        stopped = False
        for i, line in enumerate(lines):
            if args.stop_at and args.stop_at in line:
                stopped = True
            if stopped or (args.py_literals_only and not re.match(r'\s*"', line)):
                continue
            masked, saved = protect(line)
            new = masked
            for pattern, replacement in RULES:
                new = re.sub(pattern, replacement, new)
            if new != masked:
                for key, value in saved.items():
                    new = new.replace(key, value)
                print(f"{path}:{i + 1}: {line.strip()[:160]}")
                print(f"  candidate -> {new.strip()[:160]}")


if __name__ == "__main__":
    main()
