library(sf)
library(dplyr)
library(tidyr)

county_sf <- st_as_sf(maps::map("county", fill = TRUE, plot = FALSE))
county_sf <- tidyr::separate(county_sf, ID, c("state", "county"))
county_test <- filter(county_sf, state == "michigan", county == "ingham")

county_test <- st_transform(county_test, crs = 42303)

st_bbox(county_test)