# https://gdal.org/python/
# https://gis.stackexchange.com/a/200477/32531

import os
import sys
import sqlite3
import gdal
import pandas as pd
import numpy as np

def query_gpkg(src_gpkg, sql_query, src_tif, xmax, xmin, ymin, ymax, out_raster):
    '''
    gssurgo.query_gpkg(src_gpkg = "gSSURGO_MI.gpkg", sql_query = 'SELECT mukey, nonirryield_r FROM mucropyld WHERE (cropname = "Corn")', src_tif = "tifs/gSSURGO_MI.tif", xmin = 925029.1, xmax = 935594, ymin = 2214590.5, ymax = 2225584, out_raster = "tests/nonirryield_r.tif")
    '''
    
    # read data and join to raster index
    db = sqlite3.connect(src_gpkg)
    table = pd.read_sql_query(sql_query, db)
    table.mukey = table.mukey.astype(int)

    # crop original raster to bounding box so we can read in memory
    # https://gis.stackexchange.com/a/237412/32531
    ds = gdal.Open(src_tif)
    raster_res = ds.GetGeoTransform()[1]
    ds = gdal.Translate('temp.tif', ds, projWin = [xmin, ymax, xmax, ymin])
    ds = gdal.Open("temp.tif")

    nrow = ds.RasterYSize
    ncol = ds.RasterXSize

    raw_values = ds.ReadAsArray()

    pixel_values = raw_values.flatten()
    pixel_values = pd.DataFrame(pixel_values, columns = ['mukey'])
    pixel_values.mukey = pixel_values.mukey.astype(int)

    # print(table.mukey.describe())
    # print(table[table.mukey.isin([186365, 1455241])])

    pixel_values = pd.merge(left = pixel_values, right = table, how = 'left', on = 'mukey')
    pixel_values = pixel_values.iloc[:,1].values
    pixel_values = np.reshape(pixel_values, (nrow, ncol))
    # print(pixel_values)

    # create output raster
    driver = ds.GetDriver()
    out_data = driver.Create(out_raster, ncol, nrow, 1, gdal.GDT_Float32)

    out_data.SetGeoTransform(ds.GetGeoTransform())
    out_data.SetProjection(ds.GetProjection())

    out_band = out_data.GetRasterBand(1)
    out_band.WriteArray(pixel_values)
    out_band.FlushCache()

    out_data = None
    # os.remove("temp.tif")
