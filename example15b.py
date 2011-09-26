from urllib2 import urlopen
from json import load

url = 'http://datacatalog.cookcountyil.gov/api/views/2wek-2jap/rows.json'
u = urlopen(url)
response = load(u)

rowNum = 1
for rowData in response['data']:
   print "\n===== Row %d ====" % (rowNum)
   colNum = 0
   for columnMeta in response['meta']['view']['columns']:
      if columnMeta['id'] > 0:
         print columnMeta['name'], ' = ', rowData[colNum]
      colNum += 1
   rowNum +=1


