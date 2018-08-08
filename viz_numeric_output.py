import sys
import rasterio
from rasterio import plot
from matplotlib import pyplot as plt

input_tif = sys.argv[1]
output_png = sys.argv[2]

# input_tif = "tests/nonirryield_r.tif"

raster = rasterio.open(input_tif)

f, ax = plt.subplots(1, figsize=(12, 12))
ax.imshow(raster.read(1), cmap='gray')
# plt.show()
plt.savefig(sys.argv[2])