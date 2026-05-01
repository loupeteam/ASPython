"""Root ``aspython`` CLI entry point.

Usage::

    aspython <subcommand> [options...]
    aspython --help
    aspython <subcommand> --help
"""
import argparse
import sys
from typing import List, Optional

from .. import __version__
from ..logging_setup import add_log_level_argument, setup_logging

from . import (
    arsim as _arsim,
    build as _build,
    deploy_libs as _deploy_libs,
    export_libs as _export_libs,
    installer as _installer,
    package_hmi as _package_hmi,
    run_tests as _run_tests,
    safety_crc as _safety_crc,
    version as _version_cmd,
)


SUBCOMMAND_MODULES = (
    _build,
    _arsim,
    _export_libs,
    _deploy_libs,
    _safety_crc,
    _version_cmd,
    _installer,
    _package_hmi,
    _run_tests,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='aspython',
        description='Python toolkit for B&R Automation Studio projects.',
    )
    parser.add_argument('-v', '--version', action='version',
                        version=f'%(prog)s {__version__}')
    add_log_level_argument(parser)

    subparsers = parser.add_subparsers(dest='command', metavar='<command>')
    subparsers.required = True

    for module in SUBCOMMAND_MODULES:
        sub = module.add_subparser(subparsers)
        # Mirror the per-script flags from the legacy CmdLine*.py wrappers so users can
        # write either ``aspython -l DEBUG <sub>`` or ``aspython <sub> -l DEBUG``.
        add_log_level_argument(sub)

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    setup_logging(args.logLevel)
    rc = args.func(args)
    return rc if isinstance(rc, int) else 0


if __name__ == '__main__':
    sys.exit(main())
