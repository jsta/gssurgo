# https://gis.stackexchange.com/a/200477/32531

import sys
import sqlite3
import gdal
import pandas as pd
import numpy as np

# arg 1 src gpkg
# arg 2 gpkg table name
# arg 3 src tif
# arg 4 output path 
# print(sys.argv[1])
# print(sys.argv[2])
# print(sys.argv[3])
# Ex: python query_gpkg.py tests/test.gpkg dt tests/r1.tif tests/r2.tif

src_gpkg = sys.argv[1]
table_name = sys.argv[2]
src_tif = sys.argv[3]
out_raster = sys.argv[4]

# read data and join to raster index
db = sqlite3.connect(src_gpkg)
table = pd.read_sql_query("SELECT * FROM " + table_name, db)

ds = gdal.Open(src_tif)
nrow = ds.RasterYSize
ncol = ds.RasterXSize

raw_values = ds.ReadAsArray()
pixel_values = raw_values.flatten()
pixel_values = pd.DataFrame(pixel_values, columns = ['uid'])
pixel_values = pixel_values.set_index('uid').join(table.set_index('uid'))
pixel_values = pixel_values.values
pixel_values = np.reshape(pixel_values, (nrow, ncol))

# create output raster
driver = ds.GetDriver()
out_data = driver.Create(out_raster, ncol, nrow)
out_data.SetGeoTransform(ds.GetGeoTransform())
out_data.SetProjection(ds.GetProjection())

out_band = out_data.GetRasterBand(1)
out_band.WriteArray(pixel_values)
