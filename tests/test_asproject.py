"""Tests against the checked-in AsProject fixture.

These tests exercise Project's file-reading capabilities and do not require
Automation Studio to be installed.
"""
import shutil
from pathlib import Path

import pytest

from aspython import Project
from aspython.models import BuildConfig

AS_PROJECT = Path(__file__).parent / 'AsProject'


@pytest.fixture(scope='module')
def project():
    return Project(str(AS_PROJECT))


@pytest.fixture()
def project_copy(tmp_path):
    """A writable copy of AsProject for tests that modify files."""
    dest = tmp_path / 'AsProject'
    shutil.copytree(AS_PROJECT, dest, ignore=shutil.ignore_patterns('node_modules', 'Binaries'))
    return Project(str(dest))


# ---------------------------------------------------------------------------
# Project metadata
# ---------------------------------------------------------------------------

def test_project_name(project):
    assert project.name == 'AsProject'


def test_project_as_version(project):
    assert project.ASVersion == 'AS6'


def test_project_paths_exist(project):
    assert Path(project.sourcePath).is_dir()
    assert Path(project.physicalPath).is_dir()


# ---------------------------------------------------------------------------
# Build configurations
# ---------------------------------------------------------------------------

def test_build_config_names(project):
    assert set(project.buildConfigNames) == {'ARM', 'Intel'}


def test_build_configs_are_build_config_instances(project):
    for config in project.buildConfigs:
        assert isinstance(config, BuildConfig)


def test_get_config_by_name(project):
    config = project.getConfigByName('Intel')
    assert config.name == 'Intel'


def test_get_config_by_name_unknown_raises(project):
    with pytest.raises(StopIteration):
        project.getConfigByName('DoesNotExist')


# ---------------------------------------------------------------------------
# Hardware parameters
# ---------------------------------------------------------------------------

def test_get_hardware_parameter_existing(project):
    assert project.getHardwareParameter('Intel', 'ConfigurationID') == 'AsProject_Intel'


def test_get_hardware_parameter_missing_returns_empty(project):
    assert project.getHardwareParameter('Intel', 'NonExistentParam') == ''


def test_set_hardware_parameter_roundtrip(project_copy):
    original = project_copy.getHardwareParameter('Intel', 'UserPartitionSize')
    project_copy.setHardwareParameter('Intel', 'UserPartitionSize', '999')
    assert project_copy.getHardwareParameter('Intel', 'UserPartitionSize') == '999'
    project_copy.setHardwareParameter('Intel', 'UserPartitionSize', original)
    assert project_copy.getHardwareParameter('Intel', 'UserPartitionSize') == original


# ---------------------------------------------------------------------------
# Library cache
# ---------------------------------------------------------------------------

KNOWN_LOUPE_LIBS = ['errorlib', 'hmitools', 'logthat', 'stringext', 'vartools']


def test_libraries_are_cached(project):
    assert len(project.libraries) > 0


def test_known_loupe_libraries_present(project):
    names = {lib.name for lib in project.libraries}
    for lib_name in KNOWN_LOUPE_LIBS:
        assert lib_name in names, f'{lib_name} not found in cached libraries'


def test_get_library_by_name(project):
    lib = project.getLibraryByName('errorlib')
    assert lib is not None
    assert lib.name == 'errorlib'


def test_get_library_by_name_unknown_returns_none(project):
    assert project.getLibraryByName('totally_fake_lib') is None


def test_get_libraries_by_name(project):
    libs = project.getLibrariesByName(['errorlib', 'stringext'])
    assert {lib.name for lib in libs} == {'errorlib', 'stringext'}
