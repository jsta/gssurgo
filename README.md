
## Problem statement

`gSSURGO` contains multiple text format datasets referenced to a single raster grid. The raster grids are contained within file geodatabase archives and  can only be extracted using ArcGIS (using the fileGDB driver).

This repo enables subsequent open source workflows by extracting the grid and aggregating it along with the remaining data into a geopackage.

## Prereqs

* Download zip files from: https://nrcs.app.box.com/v/soils

* Have the `arcpy` python module available for the intial `tif` extraction step

* Have the `ogr2ogr` command available and working with the `GPKG` driver

## Usage

`make all`

> Do not attempt to compress the output tifs. They are still very large even with the most aggresive `gdal` compression.