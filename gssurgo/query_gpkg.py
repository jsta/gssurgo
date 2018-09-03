"""Pull gSSURGO data based on mukeys."""

# https://gdal.org/python/
# https://gis.stackexchange.com/a/200477/32531

import os
import sys
import sqlite3
import gdal
import pandas as pd
import numpy as np
from pyproj import Proj, transform
from .aoi import state_by_bbox


def query_gpkg(src_tif, gpkg_path, sql_query, out_raster):
    r"""Pull gSSURGO data based on mukeys.

    :param str src_tif: location of an AOI tif file
    :param str gpkg_path: location of folder containing state gpkg databases
    :param str sql_query: an SQL query string or location of an SQL query file
    :param str out_raster: location of the output raster

    Examples
    --------
    gssurgo.query_gpkg(src_tif = "tests/aoi.tif", gpkg_path = "gpkgs", \
                       sql_query = 'SELECT mukey, nonirryield_r \
                                    FROM mucropyld \
                                    WHERE (cropname = "Corn")', \
                                    out_raster = "tests/nonirryield_r.tif")

    """
    ds = gdal.Open(src_tif)

    gtransform = ds.GetGeoTransform()
    pixelWidth = gtransform[1]
    pixelHeight = gtransform[5]
    nrow = ds.RasterYSize
    ncol = ds.RasterXSize

    xmin = gtransform[0]
    ymax = gtransform[3]
    xmax = xmin + ncol * pixelWidth
    ymin = ymax - nrow * pixelHeight

    # https://gis.stackexchange.com/a/78944/32531
    outProj = Proj(init='epsg:4326')
    inProj = Proj('+proj=aea +lat_1=29.5 +lat_2=45.5 +lat_0=23 +lon_0=-96 \
                   +x_0=0 +y_0=0 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m \
                   +no_defs')
    xmin, ymin = transform(inProj, outProj, xmin, ymin)
    xmax, ymax = transform(inProj, outProj, xmax, ymax)

    raw_values = ds.ReadAsArray()
    pixel_values = raw_values.flatten()
    pixel_values = pd.DataFrame(pixel_values, columns = ['mukey'])
    pixel_values.mukey = pixel_values.mukey.astype(int)

    # print(table.mukey.describe())
    # print(table[table.mukey.isin([186365, 1455241])])

    # find src gpkgs
    src_gpkg = state_by_bbox(fpath = gpkg_path, ext = "gpkg", xmin = xmin,
                             xmax = xmax, ymin = ymin, ymax = ymax)

    # read data and join to raster index
    if(os.path.isfile(sql_query)):
        sql_query = open(sql_query, 'r').read()

    if(len(src_gpkg) == 1):
        db = sqlite3.connect(''.join(src_gpkg))
        table = pd.read_sql_query(sql_query, db)
        table.mukey = table.mukey.astype(int)
    else:
        db = sqlite3.connect(''.join(src_gpkg[0]))
        table1 = pd.read_sql_query(sql_query, db)
        table1.mukey = table1.mukey.astype(int)

        db = sqlite3.connect(''.join(src_gpkg[1]))
        table2 = pd.read_sql_query(sql_query, db)
        table2.mukey = table2.mukey.astype(int)

        table = table1.append(table2)

    pixel_values = pd.merge(left = pixel_values, right = table,
                            how = 'left', on = 'mukey')
    pixel_values = pixel_values.iloc[:, 1].values
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
