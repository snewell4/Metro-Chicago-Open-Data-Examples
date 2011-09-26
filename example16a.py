from urllib2 import urlopen
from json import load

url = 'http://datacatalog.cookcountyil.gov/api/views/e9qr-rmq4/rows.json'
u = urlopen(url)
response = load(u)

for columnMeta in response['meta']['view']['columns']:
	   print columnMeta['id'], ' : ', columnMeta['name']


