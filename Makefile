zips = ${wildcard *.zip}
gdbs := $(basename $(zips))
tifs := $(gdbs:.gdb=.tif)

# ME, CT, IL, IN, IA, MN, MO, NH, VT, MA, MI, NJ, NY, OH, PA, RI, WI}

.PHONY: tifs all test

test: 
	echo $(tifs)
	echo $(gdbs)

all: tifs/$(tifs)

$(gdbs): $(zips)
	unzip $<

tifs/$(tifs): $(gdbs)
	echo $@
	echo $</MapunitRaster_10m
	C:/Python27/ArcGIS10.3/python.exe pull_ssurgo_tif.py $</MapunitRaster_10m $@
	