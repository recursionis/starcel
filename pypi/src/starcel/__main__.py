"""Run `python -m starcel` -> same as `starcel`."""
import sys

from .cli import main

if __name__ == "__main__":
    sys.exit(main())
