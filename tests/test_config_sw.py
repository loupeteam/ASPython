"""Hermetic tests for CpuConfig software-configuration (.sw) resolution.

These build a throwaway ``Cpu.pkg`` on disk so the reference-resolution logic
(local file, ``Reference="true"`` with a ``..``-relative or project-root-relative
target) is exercised without needing the lpm-generated AsProject fixture.
"""
import os

from aspython import CpuConfig

NS = 'http://br-automation.co.at/AS/Package'


def _write_cpu_pkg(directory, object_xml: str) -> str:
    directory.mkdir(parents=True, exist_ok=True)
    pkg = directory / 'Cpu.pkg'
    pkg.write_text(
        '<?xml version="1.0" encoding="utf-8"?>\n'
        f'<Cpu xmlns="{NS}">\n'
        f'  <Objects>\n{object_xml}\n  </Objects>\n'
        '</Cpu>\n'
    )
    return str(pkg)


def test_local_sw_path(tmp_path):
    cpu_dir = tmp_path / 'Cfg' / 'Cpu'
    pkg = _write_cpu_pkg(
        cpu_dir,
        '    <Object Type="File" Description="Software configuration">Cpu.sw</Object>',
    )
    cfg = CpuConfig(pkg)
    assert cfg.getSoftwareConfigPath() == os.path.join(str(cpu_dir), 'Cpu.sw')


def test_reference_dotdot_relative(tmp_path):
    cpu_dir = tmp_path / 'Physical' / 'CfgB' / 'Cpu'
    pkg = _write_cpu_pkg(
        cpu_dir,
        '    <Object Type="File" Description="Software configuration" '
        'Reference="true">..\\..\\CfgA\\Cpu\\Cpu.sw</Object>',
    )
    cfg = CpuConfig(pkg)
    expected = os.path.normpath(
        os.path.join(str(cpu_dir), '..', '..', 'CfgA', 'Cpu', 'Cpu.sw'))
    assert cfg.getSoftwareConfigPath() == expected


def test_reference_project_root_relative(tmp_path):
    cpu_dir = tmp_path / 'Physical' / 'CfgB' / 'Cpu'
    pkg = _write_cpu_pkg(
        cpu_dir,
        '    <Object Type="File" Description="Software configuration" '
        'Reference="true">Physical\\CfgA\\Cpu\\Cpu.sw</Object>',
    )
    cfg = CpuConfig(pkg)
    resolved = cfg.getSoftwareConfigPath(projectRoot=str(tmp_path))
    assert resolved == os.path.join(
        str(tmp_path), 'Physical', 'CfgA', 'Cpu', 'Cpu.sw')


def test_reference_auto_detects_project_root_via_apj(tmp_path):
    (tmp_path / 'MyProj.apj').write_text('<Project/>')
    cpu_dir = tmp_path / 'Physical' / 'CfgB' / 'Cpu'
    pkg = _write_cpu_pkg(
        cpu_dir,
        '    <Object Type="File" Description="Software configuration" '
        'Reference="true">Physical\\CfgA\\Cpu\\Cpu.sw</Object>',
    )
    cfg = CpuConfig(pkg)
    # No projectRoot passed: it should be discovered from the .apj location.
    assert cfg.getSoftwareConfigPath() == os.path.join(
        str(tmp_path), 'Physical', 'CfgA', 'Cpu', 'Cpu.sw')


def test_sw_deployment_table_none_when_missing(tmp_path):
    cpu_dir = tmp_path / 'Cfg' / 'Cpu'
    pkg = _write_cpu_pkg(
        cpu_dir,
        '    <Object Type="File" Description="Software configuration">Cpu.sw</Object>',
    )
    cfg = CpuConfig(pkg)
    # The referenced Cpu.sw does not exist on disk.
    assert cfg.getSwDeploymentTable() is None
