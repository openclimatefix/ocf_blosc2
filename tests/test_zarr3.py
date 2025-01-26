"""Test the Zarr version 3 codec with the Blosc2 codec."""
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import pytest

if TYPE_CHECKING:  # pragma: no cover
    import zarr
else:
    zarr = pytest.importorskip("zarr")

import numcodecs.zarr3
import zarr.storage

from ocf_blosc2.ocf_blosc2_v3 import Blosc2

pytestmark = [
    pytest.mark.filterwarnings("ignore:Codec 'numcodecs.*' not configured in config.*:UserWarning"),
    pytest.mark.filterwarnings(
        "ignore:Numcodecs codecs are not in the Zarr version 3 specification and may not be supported by other zarr implementations." # noqa
    ),
]

get_codec_class = zarr.registry.get_codec_class
Array = zarr.Array
BytesCodec = zarr.codecs.BytesCodec
Store = zarr.abc.store.Store
MemoryStore = zarr.storage.MemoryStore
StorePath = zarr.storage.StorePath


EXPECTED_WARNING_STR = "Numcodecs codecs are not in the Zarr version 3.*"


@pytest.fixture
def store() -> StorePath:
    """Make a new in-memory store."""
    return StorePath(MemoryStore(read_only=False))


ALL_CODECS = [getattr(numcodecs.zarr3, cls_name) for cls_name in numcodecs.zarr3.__all__]


@pytest.mark.parametrize(
    "codec_class",
    [Blosc2],
)
def test_generic_compressor(
    store: StorePath, codec_class: type[numcodecs.zarr3._NumcodecsBytesBytesCodec]
):
    """Test that the generic compressor works with the Blosc2 codec."""
    data = np.arange(0, 256, dtype="uint16").reshape((16, 16))

    with pytest.warns(UserWarning, match=EXPECTED_WARNING_STR):
        a = zarr.create_array(
            store / "generic",
            shape=data.shape,
            chunks=(4, 4),
            shards=(16, 16),
            dtype=data.dtype,
            fill_value=0,
            compressors=[codec_class()],
        )

    a[:, :] = data.copy()
    np.testing.assert_array_equal(data, a[:, :])
