"""Tests for pure helpers in aspython.paths."""
import os
from unittest.mock import patch

from aspython.paths import (
    _findASBase,
    convertAsPathToWinPath,
    convertWinPathToAsPath,
    findProjectRoot,
    getASBuildPath,
    getASPath,
    getAsPathType,
    getPVITransferPath,
    resolveReferencePath,
)


def test_get_as_path_base():
    # Without any AS install present, falls back to the legacy default.
    with patch('aspython.paths.os.path.isdir', return_value=False):
        assert getASPath('base') == 'C:\\BrAutomation'


def test_get_as_path_versioned():
    with patch('aspython.paths.os.path.isdir', return_value=False):
        p = getASPath('AS49')
    assert p.endswith(os.path.join('AS49', 'Bin-en'))
    assert p.startswith('C:\\BrAutomation')


def test_find_as_base_prefers_match():
    """When AS6 lives under Program Files, _findASBase should pick it."""
    program_files = 'C:\\Program Files (x86)\\BRAutomation'

    def _fake_isdir(path: str) -> bool:
        # Pretend only the Program Files base exists, and only it has AS6.
        if path == program_files:
            return True
        if path == os.path.join(program_files, 'AS6'):
            return True
        return False

    with patch('aspython.paths.os.path.isdir', side_effect=_fake_isdir):
        assert _findASBase('AS6') == program_files


def test_find_as_base_legacy_fallback():
    with patch('aspython.paths.os.path.isdir', return_value=False):
        assert _findASBase('AS49') == 'C:\\BrAutomation'


def test_get_as_build_path():
    assert getASBuildPath('AS49').endswith('BR.AS.Build.exe')
    assert getASBuildPath('base') == getASPath('base')


def test_get_pvi_transfer_path():
    p = getPVITransferPath('V4.9')
    assert 'PVI' in p
    assert p.endswith('PVITransfer')


def test_as_path_type_relative():
    assert getAsPathType('\\Logical\\Foo') == 'relative'
    assert getAsPathType('..\\Foo') == 'relative'


def test_as_path_type_absolute():
    assert getAsPathType('C:\\Foo') == 'absolute'
    assert getAsPathType('/usr/local') == 'absolute'


def test_path_round_trip_relative():
    win = convertAsPathToWinPath('\\Logical\\Foo')
    assert win.startswith('.')
    back = convertWinPathToAsPath(win)
    assert back.startswith('\\')


# ---------------------------------------------------------------------------
# resolveReferencePath -- resolving Cpu.pkg/Package.pkg Reference="true" targets
# ---------------------------------------------------------------------------

ROOT = os.path.join('C:\\', 'proj')
BASE = os.path.join(ROOT, 'Physical', 'CfgB', 'Cpu')


def test_resolve_reference_project_root_relative_no_slash():
    # The shape seen in real cross-config .sw references.
    ref = 'Physical\\CfgA\\Cpu\\Cpu.sw'
    assert resolveReferencePath(ref, BASE, ROOT) == \
        os.path.join(ROOT, 'Physical', 'CfgA', 'Cpu', 'Cpu.sw')


def test_resolve_reference_leading_slash_is_project_root():
    ref = '\\Physical\\CfgA\\Cpu\\Cpu.sw'
    assert resolveReferencePath(ref, BASE, ROOT) == \
        os.path.join(ROOT, 'Physical', 'CfgA', 'Cpu', 'Cpu.sw')


def test_resolve_reference_dotdot_is_base_relative():
    ref = '..\\..\\CfgA\\Cpu\\Cpu.sw'
    assert resolveReferencePath(ref, BASE, ROOT) == \
        os.path.normpath(os.path.join(BASE, ref))


def test_resolve_reference_absolute_kept():
    ref = 'C:\\elsewhere\\Cpu.sw'
    assert resolveReferencePath(ref, BASE, ROOT) == os.path.normpath('C:\\elsewhere\\Cpu.sw')


def test_resolve_reference_empty():
    assert resolveReferencePath('', BASE, ROOT) == ''
    assert resolveReferencePath(None, BASE, ROOT) == ''


def test_find_project_root(tmp_path):
    proj = tmp_path / 'MyProj'
    deep = proj / 'Physical' / 'CfgA' / 'Cpu'
    deep.mkdir(parents=True)
    (proj / 'MyProj.apj').write_text('<Project/>')
    assert findProjectRoot(str(deep)) == str(proj)


def test_find_project_root_none_when_absent(tmp_path):
    deep = tmp_path / 'nope' / 'deeper'
    deep.mkdir(parents=True)
    assert findProjectRoot(str(deep)) is None
