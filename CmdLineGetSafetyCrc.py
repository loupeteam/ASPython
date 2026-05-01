'''
 * File: CmdLineGetSafetyCrc.py
 * Copyright (c) 2023 Loupe
 * https://loupe.team
 *
 * This file is part of ASPython, licensed under the MIT License.
'''
"""Backwards-compatibility shim — delegates to ``aspython safety-crc``."""
import sys
import warnings

from aspython.cli.main import main as _aspython_main


def main():
    warnings.warn(
        "CmdLineGetSafetyCrc.py is deprecated; use 'aspython safety-crc' instead.",
        DeprecationWarning, stacklevel=2,
    )
    sys.exit(_aspython_main(['safety-crc', *sys.argv[1:]]))


if __name__ == "__main__":
    main()
