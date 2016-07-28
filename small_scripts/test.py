#!/usr/bin/python

import sys
import os
from osgeo import gdal
from osgeo.gdalnumeric import *
from osgeo.gdalconst import *


def main(args):
    # basefile = "cm_pollution_2001_total_tiles.tif"
    basefile = args[0]
    outFile = args[1]  # 'out_b1.tiff'
    tmpOutFile = "derp.tif"
    original = gdal.Open(basefile, GA_ReadOnly)

    if not original:
        print "derp"
        return None

    if original.RasterXSize < 300 and original.RasterYSize < 300:
        print 'Size is ', original.RasterXSize, ',', original.RasterYSize, \
            ' translating'
        os.system('gdal_translate -of GTIFF -stats -strict -outsize 300% ' +
                  '300% ' + basefile + ' ' + tmpOutFile)
        original = gdal.Open(tmpOutFile, GA_ReadOnly)

    driver = gdal.GetDriverByName("GTiff")
    dsOut = driver.Create(outFile, original.RasterXSize,
                          original.RasterYSize, 1, gdal.GDT_Float64)

    print 'The size is ', original.RasterXSize, ',', original.RasterYSize, \
        'numer of bands = ', original.RasterCount
    # Open the dataset
    bandNum1 = 1
    band1 = original.GetRasterBand(bandNum1)
    nodataValue = band1.GetNoDataValue()
    geotransform = original.GetGeoTransform()

    print 'Pixel Size = (', geotransform[1], ',', geotransform[5], ')'
    print 'no data value: ', nodataValue

    # Read the data into numpy arrays
    data1 = numpy.array(BandReadAsArray(band1), dtype=numpy.float64)

    # The actual calculation
    dataOut = numpy.around(data1, decimals=3)
    print "Showing result of rounding"
    # print data1[10]
    # print dataOut[10]

    print "Update no data value"
    current_no_data = data1.flat[data1.argmin()]
    new_nodataValue = -9999
    if current_no_data <= new_nodataValue:
        print 'Fixing no data value'
        new_nodataValue = current_no_data - 100

    dataOut[dataOut == nodataValue] = new_nodataValue
    print "updated nodata"
     
    # print data1[10]
    # print dataOut[10]

    print original.RasterXSize
    CopyDatasetInfo(original, dsOut)
    bandOut = dsOut.GetRasterBand(1)
    BandWriteArray(bandOut, dataOut)
    bandOut.SetNoDataValue(new_nodataValue)
    print 'new no data value: '
    print bandOut.GetNoDataValue()

    # Close the datasets
    band1 = None
    original = None
    bandOut = None
    dsOut = None

    return outFile


if __name__ == "__main__" and len(sys.argv) > 2:
    main(sys.argv[1:])
else:
    print "No file provided"