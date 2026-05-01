"""Tests for pure helpers in aspython.paths."""
import os

from aspython.paths import (
    convertAsPathToWinPath,
    convertWinPathToAsPath,
    getASBuildPath,
    getASPath,
    getAsPathType,
    getPVITransferPath,
)


def test_get_as_path_base():
    assert getASPath('base') == 'C:\\BrAutomation'


def test_get_as_path_versioned():
    p = getASPath('AS49')
    assert p.endswith(os.path.join('AS49', 'Bin-en'))
    assert p.startswith('C:\\BrAutomation')


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
