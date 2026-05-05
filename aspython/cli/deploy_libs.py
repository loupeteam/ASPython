"""``aspython deploy-libs`` subcommand."""
import logging
import os

from .. import SwDeploymentTable


SUBCOMMAND = 'deploy-libs'
HELP = 'Deploy libraries to a cpu.sw deployment table.'


def add_subparser(subparsers):
    p = subparsers.add_parser(SUBCOMMAND, help=HELP, description=HELP)
    p.add_argument('-d', '--deploymentFile', type=str, required=True,
                   help='Path to the cpu.sw file')
    p.add_argument('-lf', '--libraryFolder', type=str, required=True,
                   help='Path to the folder that holds the libraries')
    p.add_argument('-lib', '--libraries', nargs='+', type=str,
                   help='Libraries to deploy (default: every library in the folder)')
    p.set_defaults(func=run)
    return p


def run(args) -> int:
    logging.debug('Updating: %s | libs: %s', args.deploymentFile, args.libraries)
    deploymentTable = SwDeploymentTable(args.deploymentFile)
    if not args.libraries:
        for library in os.listdir(args.libraryFolder):
            if library != 'Package.pkg':
                deploymentTable.deployLibrary(args.libraryFolder, library)
    else:
        for library in args.libraries:
            deploymentTable.deployLibrary(args.libraryFolder, library)
    return 0
