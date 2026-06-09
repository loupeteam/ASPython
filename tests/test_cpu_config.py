"""Tests for CpuConfig against the Cpu.pkg in the AsProject fixture."""
import shutil
from pathlib import Path

import pytest

from aspython import CpuConfig

AS_PROJECT = Path(__file__).parent / 'AsProject'
CPU_PKG = AS_PROJECT / 'Physical' / 'Intel' / '5APC4100_TGL1_000' / 'Cpu.pkg'


@pytest.fixture(scope='module')
def cpu_config():
    return CpuConfig(str(CPU_PKG))


@pytest.fixture()
def cpu_config_copy(tmp_path):
    dest = tmp_path / 'Cpu.pkg'
    shutil.copy(CPU_PKG, dest)
    return CpuConfig(str(dest))


# ---------------------------------------------------------------------------
# Reading
# ---------------------------------------------------------------------------

def test_gcc_version(cpu_config):
    assert cpu_config.gccVersion == '11.3.0'


def test_ar_version(cpu_config):
    assert cpu_config.arVersion == '6.6.2'


def test_pre_build_step_missing_returns_none(cpu_config_copy):
    del cpu_config_copy.buildElement.attrib['PreBuildStep']
    assert cpu_config_copy.preBuildStep is None


# ---------------------------------------------------------------------------
# Software-configuration (.sw) resolution
# ---------------------------------------------------------------------------

def test_software_config_path_resolves_existing_sw(cpu_config):
    sw = cpu_config.getSoftwareConfigPath()
    assert sw is not None
    assert sw.lower().endswith('.sw')
    assert Path(sw).is_file()


def test_sw_deployment_table_is_loaded(cpu_config):
    table = cpu_config.getSwDeploymentTable()
    assert table is not None
    assert 'standard' in table.libraries


# ---------------------------------------------------------------------------
# Write roundtrips
# ---------------------------------------------------------------------------

def test_set_gcc_version_roundtrip(cpu_config_copy):
    cpu_config_copy.gccVersion = '12.0.0'
    assert cpu_config_copy.gccVersion == '12.0.0'

    reloaded = CpuConfig(cpu_config_copy.path)
    assert reloaded.gccVersion == '12.0.0'


def test_set_ar_version_roundtrip(cpu_config_copy):
    cpu_config_copy.arVersion = '6.7.0'
    assert cpu_config_copy.arVersion == '6.7.0'

    reloaded = CpuConfig(cpu_config_copy.path)
    assert reloaded.arVersion == '6.7.0'


def test_set_pre_build_step_roundtrip(cpu_config_copy):
    cpu_config_copy.preBuildStep = 'echo building'
    assert cpu_config_copy.preBuildStep == 'echo building'

    reloaded = CpuConfig(cpu_config_copy.path)
    assert reloaded.preBuildStep == 'echo building'
