'''
 * File: ExportLibraries.py
 * Copyright (c) 2023 Loupe
 * https://loupe.team
 *
 * This file is part of ASPython, licensed under the MIT License.
'''
"""Deprecated parameter-file driven export — superseded by ``aspython export-libs``."""
import sys
import warnings


def main():
    warnings.warn(
        "ExportLibraries.py is deprecated; use 'aspython export-libs' instead.",
        DeprecationWarning, stacklevel=2,
    )
    sys.stderr.write(
        "ExportLibraries.py has been removed. Use 'aspython export-libs' (or the legacy "
        "CmdLineExportLib.py shim) instead.\n"
    )
    sys.exit(1)


if __name__ == "__main__":
    main()
