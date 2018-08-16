# return us state abbeviations from state that intersect a bounding box
import geopandas as gpd
from matplotlib import pyplot as plt
import glob
import re
import gdal
import os

def state_by_bbox(in_raster_path, xmax, xmin, ymin, ymax):
    '''
    Examples
    --------
    gssurgo.state_by_bbox(in_raster_path = "tifs", xmax = -82.08, xmin = -92.59, ymin = 38.12, ymax = 44.68)

    Notes
    -----
    download: http://www2.census.gov/geo/tiger/GENZ2017/shp/cb_2017_us_state_500k.zip
    `ogr2ogr -f GPKG states.gpkg cb_2017_us_state_50k.shp`
    '''

    states = gpd.read_file("states.gpkg")
    states = states[states.STATEFP.astype(int) < 60]
    states = states[~states.NAME.isin(['Hawaii', 'Alaska'])]    

    states = states.cx[xmin:xmax, ymin:ymax]

    # ax = states.plot(color='white', edgecolor='black')
    # plt.show()

    keywords = re.compile(r'.*(%s).tif' % '|'.join(states.STUSPS))

    return list(filter(keywords.match, glob.glob(in_raster_path + "*.tif")))
    
    

def aoi(in_raster_path, out_raster, xmin, ymax, xmax, ymin, src_tif=None):
    '''
    Examples
    --------

    gssurgo.aoi("temp.tif", )

    Notes
    -----    
    crop original raster to bounding box so we can read in memory
    https://gis.stackexchange.com/a/237412/32531
    '''

    if src_tif is not None:
        state_by_bbox(in_raster_path, xmax, xmin, ymin, ymax)

    ds = gdal.Open(src_tif)
    # raster_res = ds.GetGeoTransform()[1]
    ds = gdal.Translate(out_raster, ds, projWin = [xmin, ymax, xmax, ymin])
