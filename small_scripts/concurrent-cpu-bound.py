import time
import os
import glob
import numpy
import rasterio
from os.path import basename, dirname, exists


def main(infile, outfile):

    with rasterio.drivers():

        # Open the source dataset.
        with rasterio.open(infile) as src:

            # Create a destination dataset based on source params.
            # The destination will be tiled, and we'll "process" the tiles
            # concurrently.
            meta = src.meta
            del meta['transform']
            meta.update(affine=src.affine)
            meta.update(blockxsize=256, blockysize=256, tiled='yes',dtype=rasterio.uint8, compress='lzw', nodata=255)
            with rasterio.open(outfile, 'w', **meta) as dst:
                    for ij, window in dst.block_windows():
                        data = src.read(window=window)
                        result = (data).astype(rasterio.uint8)
                        dst.write(result, window=window)


main("/Users/alicia/Downloads/bra_land_cover/bra_land_cover.tif", "/Users/alicia/Downloads/bra_land_cover/new/test_2.tif")
print "finish"