'''
 * File: UnitTestTools.py
 * Copyright (c) 2023 Loupe
 * https://loupe.team
 *
 * This file is part of ASPython, licensed under the MIT License.
'''
"""Backwards-compatibility shim — use ``aspython.unittests`` instead."""
import warnings as _warnings

from aspython.unittests import UnitTestServer  # noqa: F401

_warnings.warn(
    "Importing from 'UnitTestTools' is deprecated; use 'aspython.unittests' instead.",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = ["UnitTestServer"]
