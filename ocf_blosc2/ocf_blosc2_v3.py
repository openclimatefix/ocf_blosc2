"""Zarr V3 adaption of Blosc2 codec for numcodecs."""
from numcodecs.zarr3 import _make_bytes_bytes_codec

Blosc2 = _make_bytes_bytes_codec("blosc2", "Blosc2")
