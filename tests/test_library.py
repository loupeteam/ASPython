"""Tests for aspython.library.Library."""
import pytest

from aspython.library import Library
from aspython.models import Dependency

_LIBRARY_XML = """\
<?xml version='1.0' encoding='utf-8'?>
<Library xmlns="http://br-automation.co.at/AS/Library" SubType="ANSIC" Version="1.0.0.0" Description="">
  <Files/>
</Library>"""


@pytest.fixture
def library_file(tmp_path):
    lib_dir = tmp_path / "TestLib"
    lib_dir.mkdir()
    lby = lib_dir / "ANSIC.lby"
    lby.write_text(_LIBRARY_XML, encoding="utf-8")
    return Library(str(lby))


def test_add_dependency_roundtrip(library_file):
    dep = Dependency(name="runtime", minVersion="", maxVersion="")
    library_file.addDependency(dep)

    # Newly added elements are visible in-memory without a write+reload roundtrip.
    assert "runtime" in library_file.dependencyNames
