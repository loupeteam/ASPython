"""Smoke tests: every aspython module imports cleanly and exposes its public API."""
import importlib

import pytest


SUBMODULES = [
    'aspython',
    'aspython._version',
    'aspython.returncodes',
    'aspython.models',
    'aspython.paths',
    'aspython.xml_base',
    'aspython.library',
    'aspython.package',
    'aspython.task',
    'aspython.deployment',
    'aspython.config',
    'aspython.build',
    'aspython.simulation',
    'aspython.project',
    'aspython.utils',
    'aspython.cnc',
    'aspython.unittests',
    'aspython.upgrades',
    'aspython.installer',
    'aspython.hmi',
    'aspython.logging_setup',
    'aspython.cli.main',
    'aspython.cli.build',
    'aspython.cli.arsim',
    'aspython.cli.export_libs',
    'aspython.cli.deploy_libs',
    'aspython.cli.safety_crc',
    'aspython.cli.version',
    'aspython.cli.installer',
    'aspython.cli.package_hmi',
    'aspython.cli.run_tests',
]


@pytest.mark.parametrize('mod', SUBMODULES)
def test_module_imports(mod):
    importlib.import_module(mod)


def test_public_api_surface():
    import aspython
    expected = {
        'Project', 'Library', 'Package', 'Task', 'SwDeploymentTable', 'CpuConfig',
        'BuildConfig', 'Dependency', 'LibExportInfo', 'ProjectExportInfo',
        'ASReturnCodes', 'PVIReturnCodeText', 'xmlAsFile',
        'buildASProject', 'batchBuildAsProject', 'ASProjetGetConfigs',
        'CreateARSimStructure', 'toDict',
    }
    missing = expected - set(dir(aspython))
    assert not missing, f'missing public symbols: {missing}'
