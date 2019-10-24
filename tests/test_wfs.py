import pytest  # type: ignore
import numpy as np  # type: ignore
from wfslib import _wfs  # type: ignore
from typing import NewType

# NPImage = NewType('NPImage', np.lib.npyio.NpzFile)


def test_qualitative_sub() -> None:
    cell_good: np.array = np.array([[130, 206, 207, 208, 209],
                                    [135, 207, 209, 207, 207],
                                    [137, 204, 210, 206, 207],
                                    [135, 210, 209, 208, 211],
                                    [136, 209, 208, 207, 210]])

    cell_bad: np.array = np.array([[118, 120, 125, 128, 145],
                                   [115, 143, 127, 126, 150],
                                   [117, 116, 127, 139, 140],
                                   [115, 120, 130, 139, 142],
                                   [116, 117, 125, 132, 146]])

    cell_err: np.array = np.array([[None, 120, 125, 128, 145],
                                   [115, 143, 127, 126, 150],
                                   [117, 116, 127, 139, 140],
                                   [115, 120, 130, 139, 142],
                                   [116, 117, 125, 132, 146]])

    assert _wfs.qualitative_sub(cell_good) == 1
    assert _wfs.qualitative_sub(cell_bad) == 0

    with pytest.raises(TypeError):
        _wfs.qualitative_sub(cell_err)


def test_moving_average() -> None:
    a: np.array = np.array([242, 241, 240, 239, 242, 240])
    assert (_wfs.moving_average(a) == np.array(
        [241., 240., 240.33333333, 240.33333333])).all
    assert (_wfs.moving_average(a, 5) == np.array([240.8, 240.4])).all

    assert (_wfs.moving_average(a, 10) == np.array([])).all

    # Не обрабатывается.
    # with pytest.raises(ValueError):
    #     assert (_wfs.moving_average(np.array([])) == np.array([])).all


def test_clear_extremums() -> None:

    maxes: np.array = np.array([242, 243, 241, 242, 241, 240, 239, 242, 240])

    assert _wfs.clear_extremums(maxes) == [243, 242]

    # Не обрабатывается.
    # with pytest.raises(ValueError):
    #     assert _wfs.clear_extremums(np.array([])) == []


def test_detect_start_point() -> None:
    assert _wfs.detect_start_point(10, 25, 45) == 45

    assert _wfs.detect_start_point(21, 50, 70) == 50

    with pytest.raises(TypeError):
        _wfs.detect_start_point(None, 47, 49)


def test_get_cell_parameters() -> None:
    lines: np.array = np.array([19, 49, 69, 99, 119, 149, 169, 199,
                                219, 249, 269, 299, 319, 349])

    assert _wfs.get_cell_parametrs(lines) == {"cell_width": 30, "border": 20}


def test_detect_grid_lines(load_examples) -> None:
    img_good: np.lib.npyio.NpzFile = load_examples[load_examples.files[0]]
    img_good_answ: list = [99, 99, [19, 49, 69, 99, 119, 149, 169, 199,
                                    219, 249, 269, 299, 319, 349],
                           [19, 49, 69, 99, 119, 149, 169, 199, 219,
                            249, 269, 299, 319, 349], 30.0, 20.0]

    img_bad: np.lib.npyio.NpzFile = load_examples[load_examples.files[1]]

    assert _wfs.detect_grid_lines(img_good) == img_good_answ

    # Не обрабатывается.
    # with pytest.raises(IndexError):
    #     _wfs.detect_grid_lines(img_bad)


def test_make_gridpoints(load_examples) -> None:
    img: np.lib.npyio.NpzFile = load_examples[load_examples.files[0]]

    answ: np.array = ([69, 99, 119, 149, 169, 199, 219, 249, 269, 299, 319,
                       349, 369, 399], [69, 99, 119, 149, 169, 199, 219,
                                        249, 269, 299, 319, 349, 369, 399])

    assert _wfs.make_gridpoints(img, 30, 20, [99, 99]) == answ

    # Не обрабатывается.
    # with pytest.raises(ValueError):
    #     _wfs.make_gridpoints(img, 30, 20, [-99, 99])


def test_points2grid() -> None:
    points: list = [69.0, 99, 119.0, 149, 169.0, 199, 219.0, 249, 269.0,
                    299, 319.0, 349, 369.0, 399]

    assert len(_wfs.points2grid(points, points)) == 49
