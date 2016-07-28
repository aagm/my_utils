
from os.path import basename, dirname, exists
import os
import rasterio
import numpy
import glob

# variables
path = glob.glob("/Users/alicia/Documents/prep/new/cwd/*.tif")
mypath = "/Users/alicia/Documents/prep/new/done/cwd/"
thres_val = 711.2

def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.mkdir(d)
#this reclass everything into the clases we want 
for i in path:
	with rasterio.open(i) as src:
	    array = src.read()
	    profile = src.profile 
	    profile.update(
	    	compress='lzw')
	array[array < thres_val] = 0
	array[array >= thres_val] = 255
	paths=mypath + basename(i)
	ensure_dir(paths)
	# Write to tif, using the same profile as the source
	with rasterio.open(mypath + basename(i), 'w', **profile) as dst:
		dst.write(array)