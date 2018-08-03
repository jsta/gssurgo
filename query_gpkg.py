# https://gdal.org/python/
# https://gis.stackexchange.com/a/200477/32531

import os
import sys
import sqlite3
import gdal
import pandas as pd
import numpy as np

src_gpkg = sys.argv[1]
table_name = sys.argv[2]
col_name = sys.argv[3]
src_tif = sys.argv[4]
xmin = float(sys.argv[5])
xmax = float(sys.argv[6])
ymin = float(sys.argv[7])
ymax = float(sys.argv[8])
out_raster = sys.argv[9]

# read data and join to raster index
db = sqlite3.connect(src_gpkg)
table = pd.read_sql_query("SELECT chkey, " + col_name + " FROM " + table_name, db)

# crop original raster to bounding box so we can read in memory
# https://gis.stackexchange.com/a/237412/32531
ds = gdal.Open(src_tif)
raster_res = ds.GetGeoTransform()[1]
ds = gdal.Translate('temp.tif', ds, projWin = [raster_res * xmin, raster_res * ymax, raster_res * xmax, raster_res * ymin])
ds = gdal.Open("temp.tif")

nrow = ds.RasterYSize
ncol = ds.RasterXSize

raw_values = ds.ReadAsArray()
pixel_values = raw_values.flatten()
pixel_values = pd.DataFrame(pixel_values, columns = ['chkey'])
pixel_values = pixel_values.set_index('chkey').join(table.set_index('chkey'))
pixel_values = pixel_values.values
pixel_values = np.reshape(pixel_values, (nrow, ncol))

# create output raster
driver = ds.GetDriver()
out_data = driver.Create(out_raster, ncol, nrow)

out_data.SetGeoTransform(ds.GetGeoTransform())
out_data.SetProjection(ds.GetProjection())

out_band = out_data.GetRasterBand(1)
out_band.WriteArray(pixel_values)
out_band.FlushCache()

os.remove("temp.tif")
