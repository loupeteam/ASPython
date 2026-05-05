"""``aspython version`` subcommand — read project build version from a .var file."""
import re
import sys

from .. import Project


SUBCOMMAND = 'version'
HELP = "Retrieve a project's build version (versionId) from a .var file."


def add_subparser(subparsers):
    p = subparsers.add_parser(SUBCOMMAND, help=HELP, description=HELP)
    p.add_argument('project', type=str, help='Path to AS project')
    p.add_argument('-bi', '--buildInfo', type=str, required=True,
                   help='Location of the buildInfo .var file')
    p.add_argument('--semver', dest='semVer', action='store_true',
                   help='Return the version in Semantic Version format')
    p.set_defaults(func=run)
    return p


def run(args) -> int:
    project = Project(args.project)
    versionId = project.getConstantValue(args.buildInfo, 'versionId')

    if args.semVer:
        try:
            match = re.search(r'(\d+\.\d+\.\d+).*-(\d+)-.*', versionId)
            versionId = match.group(1)
            if match.group(2) != '':
                versionId = versionId + '.' + match.group(2)
            else:
                versionId = versionId + '.0'
        except Exception:
            versionId = '0.0.0.0'

    sys.stdout.write(versionId)
    return 0
