library(rgdal)
library(raster)
library(dplyr)
library(ggplot2)

set.seed(554)

r1       <- raster(nrows=10, ncols=10, xmn=0, xmx=10, ymn = 0, ymx = 10)
data_len <- ncell(r1)
r1[]     <- seq_len(data_len)
writeRaster(r1, "tests/r1.tif", overwrite = TRUE)

dt    <- data.frame(mukey = seq_len(ncell(r1)),
                 dt = sample(1:30, data_len, replace = TRUE))
my_db <- src_sqlite("tests/test.gpkg", create = TRUE)
copy_to(my_db, dt, "dt", temporary = FALSE, overwrite = TRUE)

r2 <- r1
r2[] <- dt$dt
writeRaster(r2, "tests/r2.tif", overwrite = TRUE)
