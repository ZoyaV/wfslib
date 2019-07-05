import h5py

import pytest
import numpy as np


@pytest.fixture(scope="function")
def load_examples():
    data = np.load("data/images.npz")
    # print(data.files)
    return data

# @pytest.fixture(scope="function")
# def create_hdf5(frame):
#     a = np.zeros((1, frame.shape[0], frame.shape[1]))
#     a[0] = frame
#     with h5py.File('mtest.h5', 'w') as f:
#
#         f.create_dataset("data", data=a)
#
#     mh5 = h5py.File('mtest.h5', 'r')
#     return mh5

