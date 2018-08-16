# gSSURGO

[![Project Status: Active - The project has reached a stable, usable state and is being actively developed.](http://www.repostatus.org/badges/latest/active.svg)](http://www.repostatus.org/#active)

`gSSURGO` contains multiple text format datasets referenced to a single raster grid. **The raster grids are contained within file geodatabase archives and  can only be extracted using ArcGIS** (using the fileGDB driver).

This repo enables subsequent open source workflows by extracting the grid and aggregating it along with the remaining data into a geopackage. Specific queries of `gSSURGO` data can be constructed in `SQL` and subsequently called against a given geopackage using the `query_gpkg.py` script.

## Prereqs

* The intial `tif` (grid) extraction step requies the `arcpy` python module

* Have the python modules listed in [environment.yml](environment.yml) installed. If using Anaconda, make sure you have the **64bit** version. You can install an Anaconda virtual environment with:

```
conda env create -n gSSURGO -f environment.yml
source activate gSSURGO
```

## Installation

```
# local install
# pip install -e  . 

# development install 
pip install git+git://github.com/jsta/gssurgo.git

# development upgrade
pip install --upgrade git+git://github.com/jsta/gssurgo.git
```

## Usage

### 1. Extract tif and build gpkgs

```
extract_gssurgo_tif 'path/to/gSSURGO_STATE.gdb/MapunitRaster_10m' 'path/to/STATE.tif'
```

```
import gssurgo
gssurgo.build_gpkg("path/to/gSSURGO_STATE.gdb", "path/to/gSSURGO_STATE.gpkg")
```

### 2. Pull specific variable and merge with corresponding tif

```
gssurgo.query_gpkg(src_gpkg = "path/to/gSSURGO_MI.gpkg", sql_query = 'SELECT mukey, nonirryield_r FROM mucropyld WHERE (cropname = "Corn")', src_tif = "path/to/gSSURGO_MI.tif", xmin = 925029.1, xmax = 935594, ymin = 2214590.5, ymax = 2225584, out_raster = "tests/nonirryield_r.tif")
```

> The `sql_query` parameter must give a two column result of `mukey` and `some_variable`. The above example produces a tif of non irrigated corn yields clipped to the defined bounding box.

### 3. Visualize output

```
gssurgo.viz_numeric_output("tests/nonirryield_r.tif", "tests/nonirryield_r.png")
```

![](tests/nonirryield_r.png)
