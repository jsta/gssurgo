library(dplyr)
library(magrittr)

gpkg <- "gSSURGO_MI.gpkg"
con <- src_sqlite(gpkg)
# src_tbls(con)

  tbl(con, "mucropyld") %>%
  filter(cropname == "Corn") %>%
  select(mukey, nonirryield_r) %>%
  filter(mukey %in% 186214:267366) %>%
  show_query()
  
# SELECT `mukey`, `nonirryield_r` FROM `mucropyld` WHERE (`cropname` = 'Corn')
  
gpkg <- "tests/test.gpkg"
con <- src_sqlite(gpkg)
src_tbls(con)

tbl(con, "dt") %>%
  show_query()