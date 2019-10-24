import h5py  # type: ignore

import pytest  # type: ignore
import numpy as np  # type: ignore


@pytest.fixture(scope="function")
def load_examples() -> np.lib.npyio.NpzFile:
    data = np.load('tests/data/images.npz')
    print(type(data))
    return data
