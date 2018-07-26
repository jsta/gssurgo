
## Problem statement

The `gSURRGO` dataset is set up so that all data is referenced to a raster grid that is contained within geodatabases. These grids can only be extracted using ArcGIS (using the fileGDB driver).

This repo enables subsequent open source workflows by extracting the grid aggregating the remaining data into a geopackage format.

## Prereqs

* Download zip files from: https://nrcs.app.box.com/v/soils

* Have the `arcpy` python module available

## Usage

`make all`