"""Allow ``python -m aspython`` to invoke the CLI."""
import sys

from .cli.main import main


if __name__ == '__main__':
    sys.exit(main())
