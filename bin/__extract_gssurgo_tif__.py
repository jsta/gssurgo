import sys
try:
    import arcpy
except:
    print('could not import arcpy')    

    arcpy.CopyRaster_management(sys.argv[1], sys.argv[2])
