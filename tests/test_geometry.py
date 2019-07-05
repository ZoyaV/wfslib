import pytest
from hypothesis import given, strategies as st, settings, Verbosity, find
from hypothesis import assume

from geometry import Geometry


@given(st.text(max_size=10), st.integers(), st.integers(), st.integers(), st.integers())
def test_geometry_init(load_examples, mode, border, cell, start_point1, start_point2):
    data = load_examples

    for _ in range(len(data)):
        image = data[data.files[_]]
        geom = None
        assume(mode != 'auto' and mode != 'not_auto')
        with pytest.raises(ValueError) as excinfo:
            geom = Geometry(image, mode, border, cell, [start_point1, start_point2])
        # print(geom)
        assert geom == None



# @given(st.integers(), st.integers(), st.integers())
# def test_detect_start_point(p1, p2, p3):
#     a = sorted([p1, p2, p3])
#     with open('test.pkl', 'rb') as f:
#         image = pickle.load(f)
#     g = geometry.Geometry(image, 'not_auto')
#     assert g.detect_start_point(a[1], a[2], a[3]) == -(g.detect_start_point(-a[1], -a[2], -a[3]))

