from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import pytest

if TYPE_CHECKING:  # pragma: no cover
    import zarr
else:
    zarr = pytest.importorskip("zarr")

import zarr.storage

import numcodecs.zarr3

from ocf_blosc2.ocf_blosc2_v3 import Blosc2

pytestmark = [
    pytest.mark.skipif(zarr.__version__ < "3.0.0", reason="zarr 3.0.0 or later is required"),
    pytest.mark.filterwarnings("ignore:Codec 'numcodecs.*' not configured in config.*:UserWarning"),
    pytest.mark.filterwarnings(
        "ignore:Numcodecs codecs are not in the Zarr version 3 specification and may not be supported by other zarr implementations."
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
    return StorePath(MemoryStore(read_only=False))


ALL_CODECS = [getattr(numcodecs.zarr3, cls_name) for cls_name in numcodecs.zarr3.__all__]


@pytest.mark.parametrize("codec_class", ALL_CODECS)
def test_entry_points(codec_class: type[numcodecs.zarr3._NumcodecsCodec]):
    codec_name = codec_class.codec_name
    assert get_codec_class(codec_name) == codec_class


@pytest.mark.parametrize("codec_class", ALL_CODECS)
def test_docstring(codec_class: type[numcodecs.zarr3._NumcodecsCodec]):
    assert "See :class:`numcodecs." in codec_class.__doc__  # type: ignore[operator]


@pytest.mark.parametrize(
    "codec_class",
    [Blosc2],
)
def test_generic_compressor(
    store: StorePath, codec_class: type[numcodecs.zarr3._NumcodecsBytesBytesCodec]
):
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
