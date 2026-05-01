"""Targeted tests for aspython.project helpers."""
from aspython.project import Project


def test_parse_as_version_legacy():
    apj = '<?xml version="1.0"?>\n<?AutomationStudio Version="4.9.6.62 SP" ?>\n<Project/>'
    assert Project._parseASVersion(apj) == 'AS49'


def test_parse_as_version_as6_uses_major_only():
    apj = '<?xml version="1.0"?>\n<?AutomationStudio Version="6.0.2.45 SP" ?>\n<Project/>'
    assert Project._parseASVersion(apj) == 'AS6'


def test_parse_as_version_as6_minor_still_major_only():
    apj = '<?xml version="1.0"?>\n<?AutomationStudio Version="6.5.1.0" ?>\n<Project/>'
    assert Project._parseASVersion(apj) == 'AS6'
