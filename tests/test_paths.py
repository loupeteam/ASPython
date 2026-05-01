"""Tests for pure helpers in aspython.paths."""
import os
from unittest.mock import patch

from aspython.paths import (
    _findASBase,
    convertAsPathToWinPath,
    convertWinPathToAsPath,
    getASBuildPath,
    getASPath,
    getAsPathType,
    getPVITransferPath,
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
