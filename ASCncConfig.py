'''
 * File: ASCncConfig.py
 * Copyright (c) 2023 Loupe
 * https://loupe.team
 *
 * This file is part of ASPython, licensed under the MIT License.
'''
"""Backwards-compatibility shim — use ``aspython.cnc`` instead."""
import warnings as _warnings

from aspython.cnc import listOfProcs  # noqa: F401

__version__ = '0.0.0.1'

_warnings.warn(
    "Importing from 'ASCncConfig' is deprecated; use 'aspython.cnc' instead.",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = ["listOfProcs"]
