import sys
try:
    import arcpy
except:
    print('could not import arcpy')

def extract_tif(in_path, out_path):
    '''
    # arg 1 input path
    # arg 2 output path
    # print(sys.argv[1])
    # print(sys.argv[2])

    # C:\Python27\ArcGIS10.3\python.exe pull_ssurgo_tif.py gSSURGO_MI.gdb\MapunitRaster_10m tifs\MI.tif
    '''

    arcpy.CopyRaster_management(in_path, out_path)
