import sys
from urllib2 import urlopen
from json import load

hostname = "data.cityofchicago.org"
viewID = "htai-wnw4"
startRow = 0
numRows = 20

while True:
    url = "http://%s/api/views/%s/rows.json?method=getRows&start=%s&length=%s" % (hostname, viewID, str(startRow), str(numRows))
    response = urlopen(url)
    rows = load(response)
    numRowsRcvd = len(rows)
    if numRowsRcvd == 0:
        break
    print '\n====== %s ROWS DOWNLOADED:  ======' % (numRowsRcvd)
    for row in rows:
        print row['2609304']      # rowID for ward number
    startRow += numRows
