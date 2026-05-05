"""Centralised logging + console-mode setup for ASPython CLIs.

Replaces the duplicated ``logging.basicConfig`` + ``ctypes.windll.kernel32`` calls in every
``CmdLine*.py`` script. On non-Windows the console-mode call is a no-op.
"""
import ctypes
import logging
import sys
from typing import Optional


_LOG_LEVELS = ('DEBUG', 'INFO', 'WARNING', 'ERROR')


def _enable_windows_ansi() -> None:
    if sys.platform != 'win32':
        return
    try:
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except Exception:
        # Some environments (e.g. running under non-conhost terminals) may not support this.
        pass


def setup_logging(level: Optional[str] = None, default_level: int = logging.INFO) -> None:
    """Configure the root logger and enable ANSI escape sequences on Windows consoles."""
    logging.basicConfig(stream=sys.stderr, level=default_level)
    if level:
        upper = level.upper()
        if upper not in _LOG_LEVELS:
            raise ValueError(f'Invalid log level: {level}')
        logging.getLogger().setLevel(getattr(logging, upper))
    _enable_windows_ansi()


def add_log_level_argument(parser) -> None:
    """Add the standard ``-l/--logLevel`` flag used by every legacy ``CmdLine*`` script."""
    parser.add_argument(
        '-l', '--logLevel', type=str.upper,
        help='Log level', choices=list(_LOG_LEVELS), default='',
    )
