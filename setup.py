""" JpegXLFloatWithNaNs

JpegXlFloatWithNaNs is a codec for numcodecs for compressing image data in Zarr/Xarray

For more detailed information, please check the accompanying README.md.
"""
from pathlib import Path

from setuptools import find_packages, setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="ocf_blosc2",
    version="0.0.1",
    license="MIT",
    description="""OCF Blosc2 is a codec for numcodecs for compressing image data in Zarr/Xarray""",
    author="Jacob Bieker",
    author_email="info@openclimatefix.org",
    company="Open Climate Fix Ltd",
    install_requires=["numpy", "blosc2"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
)
