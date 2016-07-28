import os
from osgeo import gdal  
from osgeo.gdalnumeric import *  
from osgeo.gdalconst import *  
basefile =  '/Users/alicia/Projects/lab/cm_pollution_2001_total_tiles.tif'
fileName =  'out_b1.tiff'
bandNum1 = 1   
outFile = 'out.tiff'  
new_nodataValue = -9999

os.system('gdal_translate -of GTIFF -stats -strict -outsize 300% 300% '+ basefile + ' ' + fileName)
#Open the dataset  
ds1 = gdal.Open(fileName, GA_ReadOnly )  
band1 = ds1.GetRasterBand(bandNum1)
nodataValue = band1.GetNoDataValue()
geotransform = ds1.GetGeoTransform()


print 'Size is ',ds1.RasterXSize,',',ds1.RasterYSize, \
      'numer of bands = ', ds1.RasterCount
print 'Pixel Size = (',geotransform[1], ',',geotransform[5],')'
print 'no data value: ', nodataValue

#Read the data into numpy arrays  
data1 = numpy.array(BandReadAsArray(band1), dtype=numpy.float64)

#The actual calculation  
dataOut = numpy.around(data1,decimals=3)
dataOut[dataOut == nodataValue] = new_nodataValue
print data1[10]
print dataOut[10]

#Write the out file  
driver = gdal.GetDriverByName("GTiff")  
dsOut = driver.Create(outFile, ds1.RasterXSize, ds1.RasterYSize, 1, gdal.GDT_Float64)  
print ds1.RasterXSize
CopyDatasetInfo(ds1,dsOut)  
bandOut=dsOut.GetRasterBand(1)
BandWriteArray(bandOut, dataOut)  
bandOut.SetNoDataValue(new_nodataValue)
 
#Close the datasets  
band1 = None  
band2 = None  
ds1 = None  
bandOut = None  
dsOut = None  