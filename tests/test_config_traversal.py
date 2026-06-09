"""End-to-end tests for Project configuration traversal against the AsProject
fixture: Config.pkg -> Cpu.pkg -> .sw, including task-source collection.

Skipped automatically when the lpm-generated AsProject is unavailable (see
conftest.py); exercised in CI where the fixture is generated.
"""
from pathlib import Path

import pytest

from aspython import CpuConfig, SwDeploymentTable
from aspython.project import Project

AS_PROJECT = Path(__file__).parent / 'AsProject'
CONFIG = 'Intel'


@pytest.fixture(scope='module')
def project():
    return Project(str(AS_PROJECT))


def test_get_config_cpus(project):
    cpus = project.getConfigCpus(CONFIG)
    assert len(cpus) >= 1
    assert all(isinstance(c, CpuConfig) for c in cpus)


def test_get_config_sw_tables(project):
    tables = project.getConfigSwTables(CONFIG)
    assert len(tables) >= 1
    assert all(isinstance(t, SwDeploymentTable) for t in tables)
    # The deployment tables carry the real library list.
    assert any('standard' in t.libraries for t in tables)


def test_get_config_task_sources(project):
    sources = project.getConfigTaskSources(CONFIG)
    assert isinstance(sources, list)
    assert all(isinstance(s, str) and s for s in sources)
    # Should equal the concatenation of each table's taskSources.
    expected = [s for t in project.getConfigSwTables(CONFIG) for s in t.taskSources]
    assert sources == expected


def test_unknown_config_yields_nothing(project):
    assert project.getConfigCpus('NoSuchConfig') == []
    assert project.getConfigSwTables('NoSuchConfig') == []
    assert project.getConfigTaskSources('NoSuchConfig') == []
