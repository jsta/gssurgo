"""Generate a png visualization of gSSURGO output."""

import sys
import rasterio
from rasterio import plot
from matplotlib import pyplot as plt


def viz_numeric_output(input_tif, output_png):
    r"""Generate a png visualization of gSSURGO output.

    Examples
    --------
    gssurgo.viz_numeric_output("tests/nonirryield_r.tif", \
                               "tests/nonirryield_r.png")

    """
    raster = rasterio.open(input_tif)

    f, ax = plt.subplots(1, figsize=(12, 12))

    ax.imshow(raster.read(1), cmap='gray')
    plt.savefig(output_png)
    plt.show()
