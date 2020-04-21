FROM rocker/geospatial:latest

LABEL maintainer="stachel2@msu.edu"

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    python3-pip \
    python3

RUN pip3 install gssurgo

