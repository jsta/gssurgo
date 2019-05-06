import pytest

from gssurgo.aoi import (
    state_by_bbox
)


def test_query_gpkg():
    assert state_by_bbox(fpath = "tests/tifs", ext = "tif",
                         xmax = -88.34945, xmin = -88.35470,
                         ymin = 38.70095, ymax = 38.70498) == \
        ['tests/tifs/IL.tif']
