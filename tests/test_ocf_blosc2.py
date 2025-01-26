"""Unit tests for ocf_blosc2"""

import numpy as np

import ocf_blosc2


def test_roundtrip():
    """Test roundtrip encoding and decoding of a numpy array."""
    buf = np.asarray([np.nan, 0.0, 0.5, 1.0], dtype=np.float32)
    blosc2 = ocf_blosc2.Blosc2()
    comp_arr = blosc2.encode(buf)
    dest = np.empty(buf.shape, buf.dtype)
    blosc2.decode(comp_arr, out=dest)
    assert np.allclose(buf, dest, equal_nan=True)
