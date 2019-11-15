import pytest # type: ignore
from hypothesis import given, strategies as st, settings, Verbosity, find
from hypothesis import assume
from wfslib.geometry import Geometry


@given(st.text(max_size=10), st.integers(), st.integers(), st.integers(),
       st.integers())
def test_geometry_init(load_examples, mode, border, cell,
                       start_point1, start_point2) -> None:

    data = load_examples

    for _ in range(len(data)):
        image = data[data.files[_]]
        geom = None
        assume(mode != 'auto' and mode != 'not_auto')

        with pytest.raises(ValueError) as excinfo:
            geom = Geometry(image, mode, border, cell,
                            [start_point1, start_point2])

        assert geom is None
