"""List places that may need a serial comma or a comma after an introductory element.

    python comma_candidates.py <text file> [...]

Input: plain text, paragraphs separated by blank lines (export the text from the sources the
build uses). Inline math in `backticks` is masked. Nothing is changed: every candidate is decided
by hand, because the patterns also match two-item phrases and inverted sentences.
This is a heuristic scan, not a grammar parser: abbreviations may split sentences,
and valid commas later in introductory phrases may still be flagged. It neither
selects a punctuation style nor establishes that an Oxford comma is required.
"""
import argparse
import re
from pathlib import Path

from cli_io import configure_utf8_output

OPENERS = {
    "In", "At", "On", "For", "Over", "Within", "Where", "When", "If", "Since", "Because", "Although", "Though",
    "After", "Before", "Of", "Among", "Across", "Against", "Under", "Below", "Above", "Outside", "Inside",
    "Unlike", "As", "Once", "While", "Without", "With", "Compared", "Globally", "Otherwise", "Conversely",
    "Formally", "Hence", "Thus", "Therefore", "Moreover", "Here", "Then", "Yet", "So", "From", "By", "Through",
    "Along", "Between", "Beyond", "Despite", "To", "Following", "Given", "Around", "Near", "Instead", "Like",
    "Unless", "Until", "Elsewhere", "Overall", "Finally", "First", "Second", "Third", "However", "Moreover",
}
NOT_INTRODUCTORY = ("There is", "There are", "Then\n", "Among the", "At the high end", "At most")


def sentences(text: str) -> list[str]:
    text = re.sub(r"`[^`]*`", "X", text)
    out = []
    for paragraph in re.split(r"\n\s*\n", text):
        paragraph = " ".join(paragraph.split())
        out += re.split(r"(?<=[.?!])\s+(?=[A-Z])", paragraph)
    return [s for s in out if s]


def serial(sentence: str) -> list[str]:
    hits = []
    for clause in re.split(r"[;:()]", sentence):
        for m in re.finditer(r"(?<!,) (and|or) ", clause):
            before = clause[: m.start()]
            last = before.rfind(",")
            if last >= 0 and len(before[last + 1:].split()) <= 12:
                hits.append(clause[max(0, last - 70): m.end() + 40])
    return hits


def introductory(sentence: str) -> list[str]:
    hits = []
    starts = [sentence] + [m.group(1) for m in re.finditer(r"[;:] (\w[^;:]*)", sentence)]
    for start in starts:
        words = start.split()
        if not words or words[0].capitalize() not in OPENERS or start.startswith(NOT_INTRODUCTORY):
            continue
        if "," not in " ".join(words[:2]):
            hits.append(" ".join(words[:14]))
    return hits


def main() -> None:
    configure_utf8_output()
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("files", nargs="+", type=Path)
    args = parser.parse_args()
    serial_hits, intro_hits = [], []
    for path in args.files:
        for index, sentence in enumerate(sentences(path.read_text(encoding="utf-8")), 1):
            serial_hits += [f"{path} [candidate sentence {index}]: {hit}" for hit in serial(sentence)]
            intro_hits += [f"{path} [candidate sentence {index}]: {hit}" for hit in introductory(sentence)]
    print("Candidate scan only: review context and the selected style; no files are written.")
    print("=== possible serial comma: 'A, B and C' ===")
    for i, hit in enumerate(serial_hits, 1):
        print(f"S{i}: ...{hit}...")
    print("\n=== possible introductory element (may already have a valid comma) ===")
    for i, hit in enumerate(intro_hits, 1):
        print(f"I{i}: {hit}")


if __name__ == "__main__":
    main()
