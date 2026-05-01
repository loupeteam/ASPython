'''
 * File: CmdLineRunUnitTests.py
 * Copyright (c) 2023 Loupe
 * https://loupe.team
 *
 * This file is part of ASPython, licensed under the MIT License.
'''
"""Backwards-compatibility shim — delegates to ``aspython run-tests``."""
import sys
import warnings

from aspython.cli.main import main as _aspython_main


def main():
    warnings.warn(
        "CmdLineRunUnitTests.py is deprecated; use 'aspython run-tests' instead.",
        DeprecationWarning, stacklevel=2,
    )
    sys.exit(_aspython_main(['run-tests', *sys.argv[1:]]))


if __name__ == "__main__":
    main()
