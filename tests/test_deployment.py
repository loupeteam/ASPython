"""Tests for SwDeploymentTable against the cpu.sw in the AsProject fixture."""
import shutil
from pathlib import Path

import pytest

from aspython import SwDeploymentTable

AS_PROJECT = Path(__file__).parent / 'AsProject'
CPU_SW = AS_PROJECT / 'Physical' / 'Intel' / '5APC4100_TGL1_000' / 'Cpu.sw'
# deployLibrary expects the parent package folder (the one containing Package.pkg),
# not the specific library subfolder.
LOUPE_LIBS_PATH = AS_PROJECT / 'Logical' / 'Libraries' / 'Loupe'


@pytest.fixture(scope='module')
def deployment():
    return SwDeploymentTable(str(CPU_SW))


@pytest.fixture()
def deployment_copy(tmp_path):
    dest = tmp_path / 'Cpu.sw'
    shutil.copy(CPU_SW, dest)
    return SwDeploymentTable(str(dest))


# ---------------------------------------------------------------------------
# Reading the existing table
# ---------------------------------------------------------------------------

def test_libraries_list_is_non_empty(deployment):
    assert len(deployment.libraries) > 0


def test_known_as_libraries_present(deployment):
    libs = deployment.libraries
    assert 'ArEventLog' in libs
    assert 'AsBrStr' in libs
    assert 'standard' in libs


def test_task_classes_exist(deployment):
    for i in range(1, 9):
        assert deployment.find(f"TaskClass[@Name='Cyclic#{i}']") is not None


# ---------------------------------------------------------------------------
# Task enumeration (taskElements / taskNames / taskSources)
# ---------------------------------------------------------------------------

def test_task_elements_non_empty(deployment):
    assert len(deployment.taskElements) > 0


def test_task_names_align_with_elements(deployment):
    assert len(deployment.taskNames) == len(deployment.taskElements)
    assert all(isinstance(n, str) for n in deployment.taskNames)


def test_task_sources_are_truthy_and_bounded(deployment):
    sources = deployment.taskSources
    # Every reported source is a non-empty string ...
    assert all(s for s in sources)
    # ... and tasks with an empty Source are excluded, so sources cannot
    # outnumber the tasks themselves.
    assert len(sources) <= len(deployment.taskElements)


# ---------------------------------------------------------------------------
# deployLibrary
# ---------------------------------------------------------------------------

def test_deploy_library_adds_entry(deployment_copy):
    deployment_copy.deployLibrary(str(LOUPE_LIBS_PATH), 'errorlib')
    # New elements lack the AS namespace until re-read from disk.
    reloaded = SwDeploymentTable(deployment_copy.path)
    assert 'errorlib' in reloaded.libraries


def test_deploy_library_is_idempotent(deployment_copy):
    deployment_copy.deployLibrary(str(LOUPE_LIBS_PATH), 'stringext')
    count_before = deployment_copy.libraries.count('stringext')
    deployment_copy.deployLibrary(str(LOUPE_LIBS_PATH), 'stringext')
    assert deployment_copy.libraries.count('stringext') == count_before


def test_deploy_library_persists_to_disk(deployment_copy):
    deployment_copy.deployLibrary(str(LOUPE_LIBS_PATH), 'vartools')

    reloaded = SwDeploymentTable(deployment_copy.path)
    assert 'vartools' in reloaded.libraries
