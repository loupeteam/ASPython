"""Tests for the dataclass models."""
from aspython.models import BuildConfig, Dependency, LibExportInfo, ProjectExportInfo


def test_build_config_defaults():
    bc = BuildConfig('Cfg1')
    assert bc.name == 'Cfg1'
    assert bc.type == 'sg4'
    assert bc.hardware == ''
    assert bc.path == ''


def test_build_config_legacy_kwargs():
    bc = BuildConfig('Cfg1', path='/p', typ='sg4_arm', hardware='x20cp04')
    assert bc.type == 'sg4_arm'
    assert bc.path == '/p'


def test_dependency():
    d = Dependency('LoupeUI', minVersion='1.0', maxVersion='2.0')
    assert d.name == 'LoupeUI'
    assert d.minVersion == '1.0'
    assert d.maxVersion == '2.0'


def test_export_info_partition():
    info = ProjectExportInfo()
    info.addLibInfo(LibExportInfo('a', '/a'))
    info.addLibInfo(LibExportInfo('b', '/b', exception=RuntimeError('boom')))
    assert len(info.success) == 1
    assert len(info.failed) == 1
    assert info.success[0].name == 'a'
    assert info.failed[0].name == 'b'


def test_export_info_extend():
    a = ProjectExportInfo()
    a.addLibInfo(LibExportInfo('a', '/a'))
    b = ProjectExportInfo()
    b.addLibInfo(LibExportInfo('b', '/b', exception=ValueError()))
    a.extend(b)
    assert len(a.success) == 1
    assert len(a.failed) == 1
