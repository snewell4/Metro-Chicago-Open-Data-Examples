import httplib
import json
import pprint

hostName   = "datacatalog.cookcountyil.gov"
service    = "/views/INLINE/rows"
formatType = "json"
parameters = "method=index"
headers    = { "Content-type:" : "application/json" }
query      = {
             "originalViewId" : "e9qr-rmq4",
             "name" : "Inline Filter",
             "query" : {
                       "filterCondition" : {
                                           "type" : "operator",
                                           "value" : "EQUALS",
                                           "children" : [
                                                            { 
                                                            "columnId" : 2700017,
                                                            "type" : "column"
                                                            },
                                                            {
                                                            "type" : "literal",
                                                            "value" : "918"
                                                            }
                                                        ]
                                            }
                       }
             }

jsonQuery = json.dumps(query)
request = service + '.' + formatType + '?' + parameters 

conn = httplib.HTTPConnection(hostName)
conn.request("POST", request, jsonQuery, headers)
response = conn.getresponse()

if response.reason != 'OK':
	print "There was an error detected."
	print "Response status = %s.\n" % response.status
	print "Response reason = %s.\n" % response.reason
	raise SystemExit(1)

rawResponse = response.read()
jsonResponse = json.loads(rawResponse)

rowNum = 1
for rowData in jsonResponse['data']:
   print "\n======== %d =======" % (rowNum)
   colNum = 0
   for columnMeta in jsonResponse['meta']['view']['columns']:
      if columnMeta['id'] > 0:
         print columnMeta['name'], ' = ', rowData[colNum]
      colNum += 1
   rowNum += 1

