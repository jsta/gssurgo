FROM rocker/geospatial:latest

LABEL maintainer="stachel2@msu.edu"

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    python3-pip \
    python3

RUN pip3 install gssurgo

RUN Rscript -e "install.packages(c('devtools','knitr','rmarkdown','RCurl'), repos = 'https://cran.rstudio.com')"

RUN Rscript -e "devtools::install_github(c('mikejohnson51/HydroData', 'cont-limno/LAGOSNEgis'))"

RUN Rscript -e "install.packages(c('dplyr', 'maps', 'LAGOSNE', 'classInt', 'cowplot', 'sf', 'stringr', 'tidyr', 'viridisLite', 'concaveman', 'ggplot2', 'kableExtra', 'magrittr', 'broom', 'FedData', 'rlang', 'units', 'raster', 'RColorBrewer', 'forcats', 'snakecase', 'nadp', 'tibble', 'tidybayes', 'corrr', 'janitor', 'pheatmap', 'ggforce', 'ggrepel', 'curl', 'glue', 'nhdR', 'rgdal', 'scales', 'slippymath', 'renv', 'mgcViz', 'pinp', 'cdlTools', 'lwgeom', 'purrr', 'rnassqs', 'tidyselect', 'macroag', 'rmapshaper', 'reticulate', 'readxl', 'writexl', 'assertr', 'readr', 'progress', 'mapview', 'spind', 'DBI', 'dbplyr', 'RSQLite', 'brms', 'gghighlight', 'ggplotify', 'ggsn', 'gridExtra', 'gstat', 'httr', 'rnaturalearth', 'smoothr', 'sp', 'unpivotr', 'vapour', 'gdalUtils', 'Metrics', 'tabularaster', 'ggExtra', 'ggridges', 'lme4', 'merTools'), repos = 'https://cran.rstudio.com')"

RUN git clone https://github.com/CNHlakes/beyond_land_use.git
