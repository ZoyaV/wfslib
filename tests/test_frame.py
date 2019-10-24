import pytest  # type: ignore
import numpy as np  # type: ignore
from wfslib.wfs import Frame  # type: ignore
from typing import NewType
from wfslib.geometry import Geometry  # type: ignore

# NPImage = NewType('NPImage', np.lib.npyio.NpzFile)


def test_frame_cls(load_examples) -> None:
    img: np.lib.npyio.NpzFile = load_examples[load_examples.files[0]]

    geom: Geometry = Geometry(img, 'auto')
    frame: Frame = Frame(img, geom, 10)

    assert frame

    # Не обрабатывается.
    # with pytest.raises(ValueError):
    #   frame.set_image('not_image_value')

    # Не обрабатывается.
    # with pytest.raises(ValueError):
    #     Frame(img, geom, -10)
