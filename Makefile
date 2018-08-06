zips = ${wildcard *.zip}
gdbs := $(basename $(zips))
tifs := tifs/$(gdbs:.gdb=.tif)
gpkgs := $(gdbs:.gdb=.gpkg)

# ME, CT, IL, IN, IA, MN, MO, NH, VT, MA, MI, NJ, NY, OH, PA, RI, WI}

.PHONY: all test tifs clean

test_makefile:
	@echo $(gdbs)
	@echo $(tifs)	
	@echo $(gpkgs)

test_query: # has a 0.5 resolution hence 5 instead of 10 for the bbox
	Rscript tests/make_gpkg.R
	python query_gpkg.py tests/test.gpkg 'SELECT * FROM dt' tests/r1.tif 5 0 0 5 tests/dt.tif

test_gssurgo:
	python query_gpkg.py gSSURGO_MI.gpkg 'SELECT mukey, nonirryield_r FROM mucropyld WHERE (cropname = "Corn")' tifs/gSSURGO_MI.tif 967288.6 925029.1 2214590.5 2258563.5 tests/nonirryield_r.tif  

all: $(gpkgs)

tifs: $(tifs)

clean:
	-rm $(tifs)

$(gdbs): $(zips)
	unzip -u $<

$(tifs): $(gdbs) pull_ssurgo_tif.py
	echo $@
	echo $</MapunitRaster_10m
	C:/Python27/ArcGIS10.3/python.exe pull_ssurgo_tif.py $</MapunitRaster_10m $@
	gdal_translate -ot Float32 $@ temp.tif
	mv temp.tif $@
	-rm temp.tif

$(gpkgs): $(gdbs) $(tifs)
	-ogr2ogr -progress -f GPKG $@ $<
	-ogr2ogr -update -f GPKG $@ $<
	gdal_translate -of GPKG $(filter-out $<,$^) $@ -co APPEND_SUBDATASET=YES