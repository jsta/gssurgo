"""Functions for defining an area of interest (aoi)."""

import geopandas as gpd
from matplotlib import pyplot as plt
import re
import gdal
import os
import rasterio.merge
from pyproj import Proj, transform
import pkg_resources


def state_by_bbox(fpath, ext, xmax, xmin, ymin, ymax):
    r"""Find state abbrevations from a long-lat bbox.

    Examples
    --------
    gssurgo.state_by_bbox(fpath = "tifs", ext = "tif",  xmax = -88.34945, \
                          xmin = -88.35470, ymin = 38.70095, ymax = 38.70498)

    Notes
    -----
    download:
    http://www2.census.gov/geo/tiger/GENZ2017/shp/cb_2017_us_state_500k.zip
    `ogr2ogr -f GPKG states.gpkg cb_2017_us_state_50k.shp`
    """
    states = gpd.read_file(pkg_resources.resource_filename('gssurgo',
                                                           'states.gpkg'))
    states = states[states.STATEFP.astype(int) < 60]
    states = states[~states.NAME.isin(['Hawaii', 'Alaska'])]

    states = states.cx[xmin:xmax, ymin:ymax]

    # ax = states.plot(color='white', edgecolor='black')
    # plt.show()

    keyword_base = r'.*(%s).' + ext
    keywords = re.compile(keyword_base % '|'.join(states.STUSPS))
    candidate_files = [os.path.join(fpath, f) for
                       f in os.listdir(fpath) if f.endswith('.' + ext)]

    return list(filter(keywords.match, candidate_files))


def aoi(in_raster_path, out_raster, xmin, ymax, xmax, ymin, src_tif = None):
    r"""Crop original raster to bounding box so we can read in memory.

    Examples
    --------
    gssurgo.aoi(in_raster_path = "tifs", out_raster = "path/to/aoi.tif", \
                xmax = -88.34945, xmin = -88.35470, ymin = 38.70095, \
                ymax = 38.70498)

    Notes
    -----
    https://gis.stackexchange.com/a/237412/32531

    """
    if src_tif is None:
        src_tif = state_by_bbox(fpath = in_raster_path, xmax = xmax,
                                xmin = xmin, ymin = ymin, ymax = ymax,
                                ext = "tif")

    # https://gis.stackexchange.com/a/78944/32531
    inProj = Proj(init='epsg:4326')
    outProj = Proj('+proj=aea +lat_1=29.5 +lat_2=45.5 +lat_0=23 +lon_0=-96 \
                    +x_0=0 +y_0=0 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 \
                    +units=m +no_defs')
    xmin, ymin = transform(inProj, outProj, xmin, ymin)
    xmax, ymax = transform(inProj, outProj, xmax, ymax)

    if(len(src_tif) == 1):
        src_tif = ''.join(src_tif)
        ds = gdal.Open(src_tif)
        # raster_res = ds.GetGeoTransform()[1]
        ds = gdal.Translate(out_raster, ds, projWin = [xmin, ymax, xmax, ymin])
    else:
        ds = gdal.Open(''.join(src_tif[0]))
        ds = gdal.Translate("temp1.tif", ds,
                            projWin = [xmin, ymax, xmax, ymin])

        ds = gdal.Open(''.join(src_tif[1]))
        ds = gdal.Translate("temp2.tif", ds,
                            projWin = [xmin, ymax, xmax, ymin])

        # https://gist.github.com/nishadhka/9bc758129c2949a3194b79570198f544
        d1 = rasterio.open("temp1.tif")
        d2 = rasterio.open("temp2.tif")

        dest, output_transform = rasterio.merge.merge([d1, d2])

        with d1 as src:
            out_meta = src.meta.copy()
        out_meta.update({"driver": "GTiff",
                         "height": dest.shape[1],
                         "width": dest.shape[2],
                         "transform": output_transform})
        with rasterio.open(out_raster, "w", **out_meta) as dest1:
            dest1.write(dest)
