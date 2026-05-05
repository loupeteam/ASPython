"""Integration test: build the test AsProject using aspython.

Requires B&R Automation Studio to be installed. Skipped automatically when
the AS build executable cannot be found.
"""
import os
from pathlib import Path

import pytest

from aspython import Project
from aspython.paths import getASBuildPath
from aspython.returncodes import ASReturnCodes

AS_PROJECT = Path(__file__).parent / 'AsProject'
CONFIGURATION = 'Intel'


def _as_installed() -> bool:
    if not (AS_PROJECT / 'AsProject.apj').exists():
        return False
    project = Project(str(AS_PROJECT))
    build_exe = getASBuildPath(project.ASVersion)
    return os.path.isfile(build_exe)


pytestmark = pytest.mark.skipif(
    not _as_installed(),
    reason='Automation Studio not installed',
)


def test_build_starter_config():
    project = Project(str(AS_PROJECT))
    result = project.build(CONFIGURATION, buildMode='Build')
    assert result.returncode <= ASReturnCodes['Warnings'], (
        f'Build failed with return code {result.returncode}'
    )
