import time
from os.path import basename, dirname, exists
import os
import rasterio
import numpy
import glob

# variables
path = glob.glob("/Users/alicia/Documents/VS/lspop2014.tif")
mypath = "/Users/alicia/Documents/VS/new"

thres_val = 762
ramp = [500,800,900]
colouring = ["3,3,3","3,4,5","5,5,6"]
hex_colouring = ["#ffffff","#ffffff","#ffffff"]

def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.mkdir(d)

# def threshold(thres_val):
# 	for i in path:
# 		with rasterio.open(i,masked=None) as src:
# 		    array = src.read()
# 		    profile = src.profile 
# 		    profile.update(
# 		    	compress='lzw')
# 		array[array < thres_val] = 0
# 		array[array >= thres_val] = 255
# 		paths=mypath + basename(i)
# 		ensure_dir(paths)
# 		# Write to tif, using the same profile as the source
# 		with rasterio.open(mypath + basename(i), 'w', **profile) as dst:
# 			dst.write(array)
# 			src.nodatavals

for i in path:

	paths=mypath + basename(i)
	ensure_dir(paths)
	# carto_path = paths + "_cartocss.cartocss"
	with rasterio.drivers():
	    with rasterio.open(i) as src:
	        kwargs = src.meta
	        kwargs.update(
	            driver='GTiff',
	            dtype=rasterio.int16,
	            count=1,
	            compress='lzw',
	            nodata = -1,
	            bigtiff='NO' # Output will be larger than 4GB
	        )
	        nodata= src.nodatavals[0]
	        windows = src.block_windows(1)
	        with rasterio.open(paths,
	                'w',
	                **kwargs) as dst:
	            for idx, window in windows:
	                src_data = src.read_band(1, window=window)

	                # Source nodata value is a very small negative number
	                # Converting in to zero for the output raster
	                # numpy.ma.masked_equal(src_data, src.nodatavals)
	                numpy.putmask(src_data, src_data == nodata, -1)
	                dst_data = (src_data).astype(rasterio.int16)
	                dst.write_band(1, dst_data, window=window)