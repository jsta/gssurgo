FROM rocker/geospatial:latest

LABEL maintainer="stachel2@msu.edu"

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    python3-pip \
    python3

RUN pip3 install gssurgo

RUN Rscript -e "install.packages(c('devtools','knitr','rmarkdown','RCurl'), repos = 'https://cran.rstudio.com')"

RUN Rscript -e "devtools::install_github(c('mikejohnson51/HydroData', 'cont-limno/LAGOSNEgis'))"

RUN Rscript -e "install.packages(c('dplyr', 'cowplot', 'sf', 'ggplot2'), repos = 'https://cran.rstudio.com')"

RUN git clone https://github.com/CNHlakes/beyond_land_use.git
