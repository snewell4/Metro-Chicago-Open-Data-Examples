from urllib2 import urlopen
from json import load

hostname = "datacatalog.cookcountyil.gov"

pageSize = '20'
pageNum = 1 
while True:
    url = "http://%s/api/views.json?page=%s&limit=%s" % (hostname, pageNum, pageSize)
    response = urlopen(url)
    views = load(response)
    numViewsRcvd = len(views)
    if numViewsRcvd == 0:
        break
    print '\n======  PAGE %s - %s VIEWS DOWNLOADED:  ======' % (pageNum, numViewsRcvd)
    for view in views:
        print view['name']
    pageNum += 1
