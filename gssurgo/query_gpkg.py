# https://gdal.org/python/
# https://gis.stackexchange.com/a/200477/32531

import os
import sys
import sqlite3
import gdal
import pandas as pd
import numpy as np
from pyproj import Proj, transform

def query_gpkg(src_tif, gpkg_path, sql_query, out_raster):
    '''
    Examples
    --------
    gssurgo.query_gpkg(src_tif = "../tests/aoi.tif", gpkg_path = "gpkgs", sql_query = 'SELECT mukey, nonirryield_r FROM mucropyld WHERE (cropname = "Corn")', out_raster = "tests/nonirryield_r.tif")
    '''
    ds = gdal.Open(src_tif)
    
    transform = ds.GetGeoTransform()
    pixelWidth = transform[1]
    pixelHeight = transform[5]
    nrow = ds.RasterYSize
    ncol = ds.RasterXSize
    
    xmin = transform[0]
    ymax = transform[3]
    xmax = xmin + ncol * pixelWidth
    ymin = ymax - nrow * pixelHeight
    # https://gis.stackexchange.com/a/78944/32531
    outProj = Proj(init='epsg:4326')
    inProj = Proj('+proj=aea +lat_1=29.5 +lat_2=45.5 +lat_0=23 +lon_0=-96 +x_0=0 +y_0=0 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs')    
    xmin, ymin = transform(inProj, outProj, xmin, ymin)
    xmax, ymax = transform(inProj, outProj, xmax, ymax)
    
    raw_values = ds.ReadAsArray()
    pixel_values = raw_values.flatten()
    pixel_values = pd.DataFrame(pixel_values, columns = ['mukey'])
    pixel_values.mukey = pixel_values.mukey.astype(int)

    # print(table.mukey.describe())
    # print(table[table.mukey.isin([186365, 1455241])])

    # find src gpkgs
    src_gpkg = state_by_bbox(fpath = gpkg_path, ext = "gpkg", xmin = xmin, xmax = xmax, ymin = ymin, ymax = ymax)

    # read data and join to raster index
    db = sqlite3.connect(src_gpkg)
    table = pd.read_sql_query(sql_query, db)
    table.mukey = table.mukey.astype(int) 

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
