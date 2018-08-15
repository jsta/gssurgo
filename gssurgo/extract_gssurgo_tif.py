import sys
try:
    import archook
    archook.get_arcpy()
    import arcpy
except ImportError:    
    print('could not import arcpy')    

def extract_tif(in_path, out_path):
    arcpy.CopyRaster_management(in_path, out_path)
