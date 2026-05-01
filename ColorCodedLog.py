'''
 * File: ColorCodedLog.py
 * Copyright (c) 2023 Loupe
 * https://loupe.team
 *
 * This file is part of ASPython, licensed under the MIT License.
'''
"""Backwards-compatibility shim.

The old ``InitializeLogger`` / ``CustomFormatter`` API was unused inside the project, but is
preserved here. New code should call ``aspython.logging_setup.setup_logging`` instead.
"""
import warnings as _warnings

# The original implementation lived only in this module and was never imported by other
# ASPython files; preserve verbatim under a sub-module name so external callers still work.
import logging
import sys
from typing import Optional, Union


def InitializeLogger(logName: str = "main", logLevel: Union[int, str, None] = None,
                     logStringFormat: Optional[str] = None, infoColor: Optional[str] = None,
                     debugColor: Optional[str] = None, warningColor: Optional[str] = None,
                     errorColor: Optional[str] = None, criticalColor: Optional[str] = None,
                     disableColors: Optional[bool] = False):
    logger = logging.getLogger(logName)
    if logLevel:
        logger.setLevel(logLevel)

    customHandler = None
    logFormatter = None
    for handler in logger.handlers:
        if isinstance(handler.formatter, CustomFormatter):
            customHandler = handler
            logFormatter = handler.formatter
            break

    if customHandler is None:
        customHandler = logging.StreamHandler(sys.stderr)
        customHandler.setLevel(logging.DEBUG)
        logFormatter = CustomFormatter()
        customHandler.setFormatter(logFormatter)
        logger.addHandler(customHandler)

    if logStringFormat:
        logFormatter.msgFormat = logStringFormat

    if disableColors:
        logFormatter.debug = ""
        logFormatter.info = ""
        logFormatter.warning = ""
        logFormatter.error = ""
        logFormatter.critical = ""
    else:
        if debugColor:
            logFormatter.debug = debugColor
        if infoColor:
            logFormatter.info = debugColor
        if warningColor:
            logFormatter.warning = debugColor
        if errorColor:
            logFormatter.error = debugColor
        if criticalColor:
            logFormatter.critical = debugColor

    return logger


class CustomFormatter(logging.Formatter):
    defaultDebug = "\x1b[38;21m"
    defaultInfo = "\x1b[38;21m"
    defaultWarning = "\x1b[33;21m"
    defaultError = "\x1b[31;21m"
    defaultCritical = "\x1b[31;1m"
    defaultReset = "\x1b[0m"
    defaultMsgFormat = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    def __init__(self):
        self._debug = CustomFormatter.defaultDebug
        self._info = CustomFormatter.defaultInfo
        self._warning = CustomFormatter.defaultWarning
        self._error = CustomFormatter.defaultError
        self._critical = CustomFormatter.defaultCritical
        self._msgFormat = CustomFormatter.defaultMsgFormat
        self._reset = CustomFormatter.defaultReset
        self.generate()

    @property
    def debug(self):
        return self._debug

    @debug.setter
    def debug(self, value):
        self._debug = value
        self.generate()

    @property
    def info(self):
        return self._info

    @info.setter
    def info(self, value):
        self._info = value
        self.generate()

    @property
    def warning(self):
        return self._warning

    @warning.setter
    def warning(self, value):
        self._warning = value
        self.generate()

    @property
    def error(self):
        return self._error

    @error.setter
    def error(self, value):
        self._error = value
        self.generate()

    @property
    def critical(self):
        return self._critical

    @critical.setter
    def critical(self, value):
        self._critical = value
        self.generate()

    @property
    def msgFormat(self):
        return self._msgFormat

    @msgFormat.setter
    def msgFormat(self, value):
        self._msgFormat = value
        self.generate()

    @property
    def reset(self):
        return self._reset

    @reset.setter
    def reset(self, value):
        self._reset = value
        self.generate()

    def generate(self):
        self._formatDict = {
            logging.DEBUG: self.debug + self.msgFormat + self.reset,
            logging.INFO: self.info + self.msgFormat + self.reset,
            logging.WARNING: self.warning + self.msgFormat + self.reset,
            logging.ERROR: self.error + self.msgFormat + self.reset,
            logging.CRITICAL: self.critical + self.msgFormat + self.reset,
        }
        return self

    def format(self, record):
        log_fmt = self._formatDict.get(record.levelno)
        return logging.Formatter(log_fmt).format(record)


_warnings.warn(
    "Importing from 'ColorCodedLog' is deprecated; use 'aspython.logging_setup.setup_logging' instead.",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = ["InitializeLogger", "CustomFormatter"]
