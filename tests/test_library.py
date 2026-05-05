"""Tests for the Library class against real .lby files in the AsProject fixture."""
import shutil
from pathlib import Path

import pytest

from aspython import Library
from aspython.models import Dependency

AS_PROJECT = Path(__file__).parent / 'AsProject'
ERRORLIB_PATH = AS_PROJECT / 'Logical' / 'Libraries' / 'Loupe' / 'errorlib'


@pytest.fixture(scope='module')
def errorlib():
    return Library(str(ERRORLIB_PATH))


@pytest.fixture()
def errorlib_copy(tmp_path):
    dest = tmp_path / 'errorlib'
    shutil.copytree(ERRORLIB_PATH, dest)
    return Library(str(dest))


# ---------------------------------------------------------------------------
# Basic metadata
# ---------------------------------------------------------------------------

def test_library_name(errorlib):
    assert errorlib.name == 'errorlib'


def test_library_version(errorlib):
    assert errorlib.version == '1.0.0'


def test_library_type_is_binary(errorlib):
    assert errorlib.type.lower() == 'binary'


# ---------------------------------------------------------------------------
# File list
# ---------------------------------------------------------------------------

def test_file_list_is_non_empty(errorlib):
    assert len(errorlib.fileList) > 0


def test_file_list_contains_known_files(errorlib):
    names = {el.text for el in errorlib.fileList}
    assert 'ErrorLib.typ' in names
    assert 'ErrorLib.fun' in names
    assert 'ErrorLib.var' in names


# ---------------------------------------------------------------------------
# Dependencies
# ---------------------------------------------------------------------------

def test_dependency_names_non_empty(errorlib):
    assert len(errorlib.dependencyNames) > 0


def test_known_dependencies_present(errorlib):
    names = errorlib.dependencyNames
    assert 'sys_lib' in names
    assert 'AsBrStr' in names


def test_dependencies_are_dependency_instances(errorlib):
    for dep in errorlib.dependencies:
        assert isinstance(dep, Dependency)


def test_dependency_with_version_range(errorlib):
    dep = next(d for d in errorlib.dependencies if d.name == 'HMITools')
    assert dep.minVersion == '1.0.0'


# ---------------------------------------------------------------------------
# Mutation: addDependency
# ---------------------------------------------------------------------------

def test_add_dependency_roundtrip(errorlib_copy):
    new_dep = Dependency(name='TestLib', minVersion='2.0.0', maxVersion='3.0.0')
    errorlib_copy.addDependency(new_dep)
    # New elements lack the AS namespace until written and re-read, so persist first.
    errorlib_copy.write()
    reloaded = Library(errorlib_copy.path)
    assert 'TestLib' in reloaded.dependencyNames


def test_add_dependency_wrong_type_raises(errorlib_copy):
    with pytest.raises(TypeError):
        errorlib_copy.addDependency('not_a_dependency')
