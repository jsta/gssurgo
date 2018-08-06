library(rgdal)
library(raster)
library(dplyr)

r1       <- raster(nrows=20, ncols=20, xmn=0, xmx=10, ymn = 0, ymx = 10)
data_len <- ncell(r1)
r1[]     <- seq_len(data_len)
writeRaster(r1, "tests/r1.tif", overwrite = TRUE)

dt    <- data.frame(mukey = seq_len(ncell(r1)),
                 dt = sample(1:30, data_len, replace = TRUE))
my_db <- src_sqlite("tests/test.gpkg", create = TRUE)
copy_to(my_db, dt, "dt", temporary = FALSE, overwrite = TRUE)
