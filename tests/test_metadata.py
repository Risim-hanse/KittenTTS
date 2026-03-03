import sys


def test_supported_python_range():
    assert (3, 10) <= sys.version_info[:2] < (3, 13)
