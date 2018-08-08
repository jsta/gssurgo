# return us state abbeviations from state that intersect a bounding box
import geopandas as gpd
from matplotlib import pyplot as plt
import glob
import re

def state_by_bbox(xmax, xmin, ymin, ymax):
    # xmax = -82.08 
    # xmin = -92.59
    # ymin = 38.12
    # ymax = 44.68
    
    # download: http://www2.census.gov/geo/tiger/GENZ2017/shp/cb_2017_us_state_500k.zip
    # ogr2ogr -f GPKG states.gpkg cb_2017_us_state_50k.shp

    states = gpd.read_file("states.gpkg")
    states = states[states.STATEFP.astype(int) < 60]
    states = states[~states.NAME.isin(['Hawaii', 'Alaska'])]    

    states = states.cx[xmin:xmax, ymin:ymax]

    # ax = states.plot(color='white', edgecolor='black')
    # plt.show()

    keywords = re.compile(r'.*(%s).tif' % '|'.join(states.STUSPS))

    list(filter(keywords.match, glob.glob("*.tif")))
    