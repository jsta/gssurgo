import gdal

def build_gpkg(in_gdb, out_gpkg):
    src_ds = gdal.Open(in_gdb)
    ds = gdal.VectorTranslate(out_gpkg, srcDS = src_ds, format = "GPKG")
    del ds
