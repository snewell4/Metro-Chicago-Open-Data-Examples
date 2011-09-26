from urllib2 import urlopen
from json import load
import pprint

url = 'http://datacatalog.cookcountyil.gov/api/views/2wek-2jap/rows.json?meta=false'
u = urlopen(url)
response = load(u)

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(response)
