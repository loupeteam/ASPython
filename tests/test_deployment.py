"""Tests for aspython.deployment.SwDeploymentTable."""
from unittest.mock import patch

import pytest

from aspython.deployment import SwDeploymentTable

# Minimal cpu.sw with all 8 TaskClass slots and a Libraries section so that
# SwDeploymentTable.__init__ finds them all and skips its write-and-reload path.
_SW_XML = """\
<?xml version='1.0' encoding='utf-8'?>
<SwConfiguration xmlns="http://br-automation.co.at/AS/SwConfiguration" Version="1.0.0.0">
  <TaskClass Name="Cyclic#1"/>
  <TaskClass Name="Cyclic#2"/>
  <TaskClass Name="Cyclic#3"/>
  <TaskClass Name="Cyclic#4"/>
  <TaskClass Name="Cyclic#5"/>
  <TaskClass Name="Cyclic#6"/>
  <TaskClass Name="Cyclic#7"/>
  <TaskClass Name="Cyclic#8"/>
  <Libraries/>
</SwConfiguration>"""

_PATCH_PATH = "aspython.deployment.getLibraryPathInPackage"
_PATCH_TYPE = "aspython.deployment.getLibraryType"


@pytest.fixture
def sw_table(tmp_path):
    sw_path = tmp_path / "cpu.sw"
    sw_path.write_text(_SW_XML, encoding="utf-8")
    with patch(_PATCH_PATH, return_value="/fake/TestLib"), patch(_PATCH_TYPE, return_value="ANSIC"):
        return SwDeploymentTable(str(sw_path))


def test_deploy_library_adds_entry(sw_table):
    with patch(_PATCH_PATH, return_value="/fake/TestLib"), patch(_PATCH_TYPE, return_value="ANSIC"):
        sw_table.deployLibrary("/some/Libraries/MyLibs", "TestLib")

    # Newly deployed library is visible in-memory without a write+reload roundtrip.
    assert "TestLib" in sw_table.libraries
