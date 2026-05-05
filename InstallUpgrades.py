'''
 * File: InstallUpgrades.py
 * Copyright (c) 2023 Loupe
 * https://loupe.team
 *
 * This file is part of ASPython, licensed under the MIT License.
'''
"""Standalone CLI: install AS upgrades from a folder of installer .exe files.

The library helper ``installBRUpgrade`` lives in ``aspython.upgrades`` and is re-exported
here for backwards compatibility.
"""
import argparse
import ctypes
import logging
import os
import sys

from aspython._version import __version__
from aspython.logging_setup import add_log_level_argument, setup_logging
from aspython.upgrades import installBRUpgrade  # noqa: F401  (re-export)


def main():
    parser = argparse.ArgumentParser(description='Install AS upgrades')
    parser.add_argument('upgradePath', type=str,
                        help='Path to single upgrade or a folder containing upgrades')
    parser.add_argument('-brp', '--brpath', type=str, default='C:\\BrAutomation',
                        help='Global AS install path')
    parser.add_argument('-asp', '--aspath', type=str,
                        help='AS install path for the desired AS version')
    parser.add_argument('-r', '--recursive', action='store_true',
                        help='Recursively search for upgrades in the upgrade path')
    add_log_level_argument(parser)
    parser.add_argument('-v', '--version', action='version',
                        version=f'%(prog)s {__version__}')
    args = parser.parse_args()
    setup_logging(args.logLevel)

    logging.debug('upgrades path: %s | brpath: %s | aspath: %s', args.upgradePath, args.brpath, args.aspath)

    try:
        is_admin = os.getuid() == 0
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

    logging.debug('Terminal is admin: %i', is_admin)
    if not is_admin:
        logging.error('Admin privileges required. Open terminal as Administrator')
        sys.exit(1)

    if os.path.isdir(args.upgradePath):
        os.chdir(args.upgradePath)
        if args.recursive:
            for root, _dirs, files in os.walk(args.upgradePath):
                for upgrade in files:
                    if upgrade.lower().endswith('.exe'):
                        installBRUpgrade(os.path.join(root, upgrade), args.brpath, args.aspath)
        else:
            for upgrade in os.listdir():
                if os.path.isfile(upgrade) and upgrade.lower().endswith('.exe'):
                    installBRUpgrade(upgrade, args.brpath, args.aspath)
    elif os.path.isfile(args.upgradePath) and args.upgradePath.lower().endswith('.exe'):
        os.chdir(os.path.dirname(args.upgradePath))
        installBRUpgrade(args.upgradePath, args.brpath, args.aspath)
    else:
        logging.error('Path provided is neither an upgrade nor a directory: ' + args.upgradePath)
        sys.exit(args.upgradePath + ' is not a valid AS upgrade')

    sys.exit(0)


if __name__ == "__main__":
    main()
