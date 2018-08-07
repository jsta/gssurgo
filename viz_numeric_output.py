import sys
import rasterio
from rasterio import plot
from matplotlib import pyplot as plt

input_tif = sys.argv[1]

# input_tif = "tests/nonirryield_r.tif"

raster = rasterio.open(input_tif)
plot.show(raster)
