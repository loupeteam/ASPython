import subprocess
import sys
from pathlib import Path

import pytest

# Make the repo-root packages importable when running ``pytest`` without an editable install.
_repo_root = Path(__file__).resolve().parent.parent
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))

AS_PROJECT = Path(__file__).parent / 'AsProject'

# Packages to install individually — lpm only deploys when a specific package
# is named; a plain ``lpm install`` (no args) downloads to node_modules but
# does not deploy project files.
_LPM_PACKAGES = [
    'librarybuilderproject@1.0.0',
    'firstinitprog',
    'stringext',
]


def _run_lpm(*args, **kwargs):
    """Run an lpm command. shell=True is required on Windows (.cmd file)."""
    subprocess.run(' '.join(['lpm', *args]), check=True, shell=True, **kwargs)


def pytest_configure(config):
    """Generate the AsProject fixture if it hasn't been set up yet."""
    if (AS_PROJECT / 'AsProject.apj').exists():
        return

    AS_PROJECT.mkdir(exist_ok=True)
    sys.stderr.write('\nAsProject not found — generating via lpm...\n')

    try:
        _run_lpm('-s', 'init', cwd=AS_PROJECT)
        for package in _LPM_PACKAGES:
            sys.stderr.write(f'  lpm install {package}\n')
            _run_lpm('-s', 'install', package, cwd=AS_PROJECT)
    except FileNotFoundError:
        sys.stderr.write(
            'ERROR: lpm not found.\n'
            'Install it from: https://loupeteam.github.io/LoupeDocs/tools/lpm.html\n'
            'AsProject-dependent tests will fail.\n'
        )
    except subprocess.CalledProcessError as exc:
        sys.stderr.write(
            f'ERROR: lpm setup failed (exit {exc.returncode}).\n'
            'AsProject-dependent tests will fail.\n'
        )


# Files whose tests all require a fully-generated AsProject (lpm).
_AS_PROJECT_DEPENDENT = {
    'test_asproject.py',
    'test_build.py',
    'test_cpu_config.py',
    'test_deployment.py',
    'test_library.py',
}


def pytest_collection_modifyitems(config, items):
    """Skip AsProject-dependent tests when the fixture project is not set up."""
    if (AS_PROJECT / 'AsProject.apj').exists():
        return
    skip = pytest.mark.skip(reason='AsProject not available (lpm not installed)')
    for item in items:
        if Path(item.fspath).name in _AS_PROJECT_DEPENDENT:
            item.add_marker(skip)
