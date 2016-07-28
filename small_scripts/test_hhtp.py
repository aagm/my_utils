import urllib2
import urllib
import json
# Specify the url


query_args = { 'q':'query string', 'foo':'bar', 'format':'json' } # you have to pass in a dictionary  

encoded_args = urllib.urlencode(query_args)

print 'Encoded:', encoded_args

url = 'http://api.worldbank.org/countries/all/indicators/SP.POP.TOTL?' + encoded_args
my_dict = json.loads('urllib2.urlopen(url).read()')

print my_dict