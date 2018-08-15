import sys
try:
    import arcpy
except:
    print('could not import arcpy')

    # C:\Python27\ArcGIS10.3\python.exe pull_ssurgo_tif.py gSSURGO_MI.gdb\MapunitRaster_10m tifs\MI.tif    

    arcpy.CopyRaster_management(sys.argv[1], sys.argv[2])
