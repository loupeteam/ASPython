"""CLI smoke tests: every subcommand wires up and ``--help`` exits 0."""
import subprocess
import sys

import pytest


SUBCOMMANDS = [
    'build',
    'arsim',
    'export-libs',
    'deploy-libs',
    'safety-crc',
    'version',
    'installer',
    'package-hmi',
    'run-tests',
]


def _run(args):
    return subprocess.run(
        [sys.executable, '-m', 'aspython', *args],
        capture_output=True, text=True,
    )


def test_root_help():
    proc = _run(['--help'])
    assert proc.returncode == 0
    for sub in SUBCOMMANDS:
        assert sub in proc.stdout


def test_root_version():
    from aspython import __version__
    proc = _run(['--version'])
    assert proc.returncode == 0
    assert __version__ in proc.stdout


@pytest.mark.parametrize('sub', SUBCOMMANDS)
def test_subcommand_help(sub):
    proc = _run([sub, '--help'])
    assert proc.returncode == 0, proc.stderr
    assert sub in proc.stdout or 'usage' in proc.stdout.lower()


def test_unknown_subcommand_fails():
    proc = _run(['totally-not-a-real-command'])
    assert proc.returncode != 0


def test_legacy_astools_shim_imports():
    """The deprecated ``ASTools`` re-export must still expose Project & friends."""
    proc = subprocess.run(
        [sys.executable, '-W', 'ignore::DeprecationWarning', '-c',
         'import ASTools; '
         'assert hasattr(ASTools, "Project"); '
         'assert hasattr(ASTools, "Library"); '
         'assert hasattr(ASTools, "buildASProject"); '
         'assert hasattr(ASTools, "ASReturnCodes")'],
        capture_output=True, text=True,
    )
    assert proc.returncode == 0, proc.stderr
