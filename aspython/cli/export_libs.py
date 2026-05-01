"""``aspython export-libs`` subcommand."""
import logging
import os.path
import shutil
import sys
from typing import List

from .. import Project, Library
from ..returncodes import ASReturnCodes


SUBCOMMAND = 'export-libs'
HELP = 'Export libraries from an AS project (binary or source).'


def add_subparser(subparsers):
    p = subparsers.add_parser(SUBCOMMAND, help=HELP, description=HELP)
    p.add_argument('project', type=str, help='Path to AS project')
    p.add_argument('-dest', '--destination', type=str,
                   help='Destination path for exported libraries')
    p.add_argument('-c', '--configuration', nargs='+', type=str,
                   help='AS configuration(s)')
    p.add_argument('-wl', '--whitelist', type=str, nargs='+', default='',
                   help='Desired libraries (trumps the blacklist)')
    p.add_argument('-bl', '--blacklist', type=str, nargs='+', default='',
                   help='Ignored libraries (glob style: *myLibName*)')
    p.add_argument('-o', '--overwrite', action='store_true',
                   help='Overwrite previously-exported libraries')
    p.add_argument('-source', '--sourceFile', action='store_true',
                   help='Export libraries as source')
    p.add_argument('-bm', '--buildMode', type=str, default='None',
                   choices=['Rebuild', 'Build', 'BuildAndTransfer', 'BuildAndCreateCompactFlash', 'None'],
                   help='Type of build in AS')
    p.add_argument('-iv', '--includeVersion', action='store_true',
                   help='Include version number in folder structure')
    p.set_defaults(func=run)
    return p


def run(args) -> int:
    buildStatus = None
    libBuildConfig: List = []

    logging.debug('Project: %s | configs: %s | overwrite=%s | source=%s | iv=%s | bm=%s',
                  args.project, args.configuration, args.overwrite, args.sourceFile,
                  args.includeVersion, args.buildMode)
    logging.debug('whitelist=%s blacklist=%s', args.whitelist, args.blacklist)

    if args.destination is None:
        args.destination = os.path.join(os.path.dirname(args.project), '..', 'Exports')
    logging.debug('Export destination: %s', args.destination)

    project = Project(args.project)

    for buildConfig in project.buildConfigs:
        if args.configuration is not None and buildConfig.name in args.configuration:
            libBuildConfig.append(buildConfig)

    if not libBuildConfig:
        logging.error('\033[31mNot a configuration in specified project: %s\033[0m', str(args.configuration))
        sys.exit('Configuration passed in is not part of AS project')

    libBuildConfigNames = [config.name for config in libBuildConfig]
    for name in args.configuration:
        if name not in libBuildConfigNames:
            logging.error('Configuration name does not exist in project: %s', name)

    if args.buildMode != 'None':
        for config in args.configuration:
            buildStatus = project.build(config, buildMode=args.buildMode, simulation=False)
            if buildStatus.returncode > ASReturnCodes['Warnings']:
                sys.exit(f'Build failed for config {config}')
            logging.debug('Building of %s Complete!', config)

    if args.buildMode == 'None' or buildStatus.returncode <= ASReturnCodes['Errors']:
        results = project.exportLibraries(
            args.destination, overwrite=args.overwrite, buildConfigs=libBuildConfig,
            blacklist=args.blacklist, whitelist=args.whitelist,
            binary=not args.sourceFile, includeVersion=args.includeVersion,
        )
        for result in results.failed:
            logging.error('\033[31mFailed to export %s to %s because %s\033[0m',
                          result.name, result.path, result.exception)
            try:
                shutil.rmtree(result.path, onerror=Library._rmtreeOnError)
            except FileNotFoundError:
                logging.debug('Failed to delete failed export lib, does not exist: %s', result.path)
            except Exception:
                logging.exception('Failed to delete: %s', result.path)

    logging.info('Export Complete!')
    return 0
