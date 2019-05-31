""" Tests for checksum """

import hashlib
import itertools
import pytest
from ubiquerg import checksum

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"


def pytest_generate_tests(metafunc):
    """ Dynamic test case generation/parameterization for this module. """
    if "size1" in metafunc.fixturenames and "size2" in metafunc.fixturenames:
        metafunc.parametrize(
            ["size1", "size2"], itertools.product([1, 4], [2, 8]))
    if "lines" in metafunc.fixturenames:
        metafunc.parametrize("lines", [[], ["line1"], ["line1", "line2"]])


def test_checksum(size1, size2, lines, tmpdir):
    """ Checksum result matches expectation and is blocksize-agnostic """
    fp = tmpdir.join("temp-data.txt").strpath
    data = "\n".join(lines)
    with open(fp, 'w') as f:
        f.write(data)
    exp = hashlib.new("md5", data.encode("utf-8")).hexdigest()
    res1 = checksum(fp, size1)
    res2 = checksum(fp, size2)
    assert exp == res1
    assert res1 == res2
    assert res2 == exp


def test_nonexistent_path(tmpdir):
    """ Nonexistent path to checksum is erroneous. """
    with pytest.raises(IOError):
        checksum(tmpdir.join("does-not-exist.txt").strpath)