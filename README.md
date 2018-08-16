# gssurgo

[![PyPiVersion](https://img.shields.io/pypi/v/georasters.svg)](https://pypi.python.org/pypi/georasters/)[![Project Status: Active - The project has reached a stable, usable state and is being actively developed.](http://www.repostatus.org/badges/latest/active.svg)](http://www.repostatus.org/#active)

The `gSSURGO` data product contains multiple text format datasets referenced to a single raster grid. **The raster grids are contained within file geodatabase archives and  can only be extracted using ArcGIS** (using the fileGDB driver).

This repo enables subsequent open source workflows with `gSSURGO` by extracting grids and aggregating the remaining data into a geopackage. This package enables specific queries of `gSSURGO` data, which are constructed in `SQL`, and subsequently merged with its corresponding (raster) grid.

## Prereqs

* The intial `tif` (grid) extraction step requies the `arcpy` python module. This step assumes that a python executable linked to `arcpy` can be found at `C:\Python27\ArcGIS10.3\python.exe`. Edit [bin/extract_gssurgo_tif](bin/extract_gssurgo_tif) to enable alternate locations.

* Remaining operations require a number of dependencies listed in [environment.yml](environment.yml) and [requirements.txt](requirements.txt). If using Anaconda, make sure you have the **64bit** version. You can install an Anaconda virtual environment with:

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
# pip install --upgrade git+git://github.com/jsta/gssurgo.git
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
