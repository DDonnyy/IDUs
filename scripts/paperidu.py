"""Compatibility entry point for the former Paperidu CLI. Use idus.py for new integrations."""

import sys

from idus import main


if __name__ == "__main__":
    sys.exit(main())
