library(sf)
library(dplyr)
library(tidyr)

county_sf <- st_as_sf(maps::map("county", fill = TRUE, plot = FALSE))
county_sf <- tidyr::separate(county_sf, ID, c("state", "county"))
county_test <- filter(county_sf, state == "michigan", county == "ingham")

county_test <- st_transform(county_test, crs = 42303)

bbox <- st_bbox(county_test)

shrink_bbox <- function(bbox, fact = 2){
  bbox[3] <- bbox[1] + ((bbox[3] - bbox[1]) / fact)
  bbox[4] <- bbox[2] + ((bbox[4] - bbox[2]) / fact)
  bbox
}

cat(as.vector(shrink_bbox(bbox, 4)[c(3, 1, 2, 4)]))
