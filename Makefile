zips = ${wildcard *.zip}
gdbs := $(basename $(zips))
tifs := tifs/$(gdbs:.gdb=.tif)
gpkgs := $(gdbs:.gdb=.gpkg)

# ME, CT, IL, IN, IA, MN, MO, NH, VT, MA, MI, NJ, NY, OH, PA, RI, WI}

.PHONY: all test gpackages

gpackages: $(gpkgs)
	echo $<

test:
	@echo $(gdbs)
	@echo $(tifs)	
	@echo $(gpkgs)

all: tifs/$(tifs)

$(gdbs): $(zips)
	unzip -u $<

$(tifs): $(gdbs)
	echo $@
	echo $</MapunitRaster_10m
	C:/Python27/ArcGIS10.3/python.exe pull_ssurgo_tif.py $</MapunitRaster_10m $@

$(gpkgs): $(gdbs) $(tifs)
	-ogr2ogr -progress -f GPKG $@ $<
	-ogr2ogr -update -f GPKG $@ $<
	gdal_translate -of GPKG $(filter-out $<,$^) $@