import time
from os.path import basename, dirname, exists
import os
import rasterio
import numpy
import glob


# With this script i'm gonna cover treatment of all rasters to control the interpolation mess that is carto right now.

# Global variables definition
path_in = glob.glob("/Users/alicia/Downloads/cwd/*.tif")
dir_out = "/Users/alicia/Downloads/cwd/new/"

thres_val = 750
ramp = [500,800,900]
colouring = ["3,3,3","3,4,5","5,5,6"]
hex_colouring = ["#ffffff","#ffffff","#ffffff"]

# Functions definition
# Ensures the existance of a path and if it is not there it creates it.
def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.mkdir(d)
#Print the cartocss into a file on the same folder as the new data
def print_cartocss(dir,text):
	with open(dir, 'w') as the_file:
	    the_file.write(text)

def coloring_generator(vals, text, is_hex):
	if is_hex:
		return map(lambda x: text + str(x) +", ", vals)
	else:
		return map(lambda x: text + x +",1))", vals)

def create_cartocss(vals, colors, mode, is_hex):
	body = "{raster-opacity:1; raster-scaling:near; raster-colorizer-default-mode:" + mode + "; raster-colorizer-default-color:  transparent; raster-colorizer-epsilon:0.41; raster-colorizer-stops: "
	RGBA = "rgba("
	STOP ="stop("
	if is_hex:
		colouring = map(lambda x: x +")", colors)
	else:
		colouring = coloring_generator(colors,RGBA,False)
	
	stops = coloring_generator(vals,STOP,True)
	former =" ".join(numpy.core.defchararray.add(stops, colouring))
	return  body + former + '}'


def threshold(infile, outfile,thres_val):
    with rasterio.drivers():
        # Open the source dataset.
        with rasterio.open(infile, masked=None) as src:
            # Create a destination dataset based on source params.
            # The destination will be tiled, and we'll "process" the tiles
            # concurrently.
            meta = src.profile.copy()
            meta.update(affine=src.affine)
            meta.update(blockxsize=256, blockysize=256, tiled='yes', compress='lzw',nodata=0, dtype=rasterio.uint8)
            with rasterio.open(outfile, 'w', **meta) as dst:
                    for ij, window in dst.block_windows():
                    	data = src.read(window=window)
                    	data[data < thres_val] = 0
                    	data[data >= thres_val] = 255
                        dst.write(data.astype(rasterio.uint8), window=window)

def interpolation(infile, outfile,thres_val):
    with rasterio.drivers():
        # Open the source dataset.
        with rasterio.open(infile, masked=None) as src:
            # Create a destination dataset based on source params.
            # The destination will be tiled, and we'll "process" the tiles
            # concurrently.
            meta = src.profile.copy()
            meta.update(affine=src.affine)
            meta.update(blockxsize=256, blockysize=256, tiled='yes', compress='lzw',nodata=0, dtype=rasterio.uint8)
            with rasterio.open(outfile, 'w', **meta) as dst:
                    for ij, window in dst.block_windows():
                        data = src.read(window=window)
                        result = (data).astype(rasterio.uint8)
                        dst.write(result, window=window)

def categorical(infile, outfile,thres_val):
    with rasterio.drivers():
        # Open the source dataset.
        with rasterio.open(infile) as src:
            # Create a destination dataset based on source params.
            # The destination will be tiled, and we'll "process" the tiles
            # concurrently.
            meta = src.meta
            del meta['transform']
            meta.update(affine=src.affine)
            meta.update(blockxsize=256, blockysize=256, tiled='yes',dtype=rasterio.uint8, compress='lzw', nodata=0)
            with rasterio.open(outfile, 'w', **meta) as dst:
                    for ij, window in dst.block_windows():
                        data = src.read(window=window)
                        result = (data).astype(rasterio.uint8)
                        dst.write(result, window=window)

def thres_submain(path_in,dir_out,reqid,thres_val):
	for i in path_in:
		dst_out=dir_out + basename(i)
		carto_path = dir_out + os.path.splitext(basename(i))[0] + ".cartocss"
		ensure_dir(dst_out)
		threshold(i, dst_out,thres_val)
		cartocss = create_cartocss([255],['#fabada'], 'exact', True)
		print_cartocss(carto_path,cartocss)

def inter_submain(path_in,dir_out,reqid,thres_val):
	for i in path_in:
		dst_out=dir_out + basename(i)
		carto_path = dir_out + os.path.splitext(basename(i))[0] + ".cartocss"
		ensure_dir(dst_out)
		interpolation(i, dst_out,thres_val)
		cartocss = create_cartocss([255],['#fabada'], 'exact', True)
		print_cartocss(carto_path,cartocss)

def cat_submain(path_in,dir_out,reqid,thres_val):
	for i in path_in:
		dst_out=dir_out + basename(i)
		carto_path = dir_out + os.path.splitext(basename(i))[0] + ".cartocss"
		ensure_dir(dst_out)
		categorical(i, dst_out,thres_val)
		cartocss = create_cartocss([255],['#fabada'], 'exact', True)
		print_cartocss(carto_path,cartocss)

def main(path_in,dir_out,reqid,thres_val):
	if reqid == 'threshold':
		thres_submain(path_in,dir_out,reqid,thres_val)
		print "Ready"
	elif reqid == 'interpolation':
		inter_submain(path_in,dir_out,reqid,thres_val)
		print "Ready"
	elif reqid == 'categorical':
		cat_submain(path_in,dir_out,reqid,thres_val)
		print "Ready"
	else:
		raise ValueError('reqid is not valid')


main(path_in,dir_out,'threshold',thres_val)




