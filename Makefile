zips = ${wildcard *.zip}
gdbs := $(basename $(zips))
tifs := tifs/$(gdbs:.gdb=.tif)
gpkgs := $(gdbs:.gdb=.gpkg)

# ME, CT, IL, IN, IA, MN, MO, NH, VT, MA, MI, NJ, NY, OH, PA, RI, WI}

.PHONY: all test tifs clean

test:
	@echo $(gdbs)
	@echo $(tifs)	
	@echo $(gpkgs)

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