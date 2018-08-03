import sys
import arcpy

# arg 1 input path
# arg 2 output path
# print(sys.argv[1])
# print(sys.argv[2])

# C:\Python27\ArcGIS10.3\python.exe pull_ssurgo_tif.py gSSURGO_MI.gdb\MapunitRaster_10m .\MI.tif

arcpy.CopyRaster_management(sys.argv[1], sys.argv[2])
