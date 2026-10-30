"""Keep helper output readable when Windows pipes use a legacy system encoding."""

import sys


def configure_utf8_output():
    """Use UTF-8 for CLI output; leave host-provided in-memory streams alone."""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding="utf-8")
