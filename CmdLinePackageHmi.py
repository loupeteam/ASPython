'''
 * File: CmdLinePackageHmi.py
 * Copyright (c) 2023 Loupe
 * https://loupe.team
 *
 * This file is part of ASPython, licensed under the MIT License.
'''
"""Backwards-compatibility shim — delegates to ``aspython package-hmi``."""
import sys
import warnings

from aspython.cli.main import main as _aspython_main


def main():
    warnings.warn(
        "CmdLinePackageHmi.py is deprecated; use 'aspython package-hmi' instead.",
        DeprecationWarning, stacklevel=2,
    )
    sys.exit(_aspython_main(['package-hmi', *sys.argv[1:]]))


if __name__ == "__main__":
    main()
