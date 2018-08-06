# gSSURGO

[![Project Status: Active - The project has reached a stable, usable state and is being actively developed.](http://www.repostatus.org/badges/latest/active.svg)](http://www.repostatus.org/#active)

`gSSURGO` contains multiple text format datasets referenced to a single raster grid. The raster grids are contained within file geodatabase archives and  can only be extracted using ArcGIS (using the fileGDB driver).

This repo enables subsequent open source workflows by extracting the grid and aggregating it along with the remaining data into a geopackage.

## Prereqs

* Download zip files from: https://nrcs.app.box.com/v/soils

* Have the `arcpy` python module available for the intial `tif` extraction step

* Have the `ogr2ogr` command available and working with the `GPKG` driver

* Have the python modules listed in [environment.yml](environment.yml) installed. If using Anaconda, make sure you have the **64bit** version. You can install an Anaconda virtual environment with:

```
conda env create -n gSSURGO -f environment.yml
source activate gSSURGO
```

## Usage

### 1. Extract tifs and build gpkg
`make all`

> Do not attempt to compress the output tifs. They are still very large even with the most aggresive `gdal` compression.

### 2. Pull specific variable and merge with corresponding tif

Compose an SQL query that give a two column result of `mukey` and `some_variable`. For example, `'SELECT mukey, nonirryield_r FROM mucropyld WHERE (cropname = "Corn")'`. Pass this query to `query_gpkg.py` along with a bounding box given by `xmax`, `xmin`, `ymin`, `ymax`:

```
python query_gpkg.py gSSURGO_MI.gpkg 'SELECT mukey, nonirryield_r FROM mucropyld WHERE (cropname = "Corn")' tifs/gSSURGO_MI.tif 967288.6 925029.1 2214590.5 2258563.5 nonirryield_r.tif
```

> See more SQL query examples in [construct_sql.R](construct_sql.R).

### 3. Visualize output

