from itertools import islice
import numpy as np

import py_gd._cm_listed
import py_gd._color_data
import py_gd


def test_init_simple():
    """
    simplest possible initialization -- no preset color palette
    """
    img = py_gd.Image(width=400, height=400, preset_colors=None)
    assert img

print(dir(py_gd))
test_init_simple()