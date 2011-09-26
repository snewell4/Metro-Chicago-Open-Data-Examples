#
#  getview - Prints the metadata for a view
#
#  args:     <hostname> <viewID>
#            If <hostname> is "-cook", use the Cook County Data Portal host name
#            If <hostname> is "-chicago", use the City of Chicago Data Portal host name
#            If <hostname> is "-ill", use the State of Illinois Data Portal host name
#            Other <hosthame> is the host name for the Socrata site.  Do not include "http://"
#            <viewID> is the 9 character Socrata view (aka dataset) ID.  Format is:  "cccc-cccc"
#
#  output:   An indented print the response from /api/views/<viewID>. 
#
import sys
from urllib2 import urlopen, URLError, HTTPError
from json import load
import pprint


hostNameChicago = "data.cityofchicago.org"
hostNameCook = "datacatalog.cookcountyil.gov"
hostNameIll = "data.illinois.gov"

if len(sys.argv) != 3:
	sys.stderr.write("Usage: python %s [-chicago | -cook | -ill | <hostname>] <viewID>\n" % sys.argv[0])
	raise SystemExit(1)

if sys.argv[1] == "-chicago":
	hostName = hostNameChicago
elif sys.argv[1] == "-cook":
	hostName = hostNameCook
elif sys.argv[1] == "-ill":
	hostName = hostNameIll
else:
	hostName = sys.argv[1]

viewID = sys.argv[2]
url = "http://%s/api/views/%s.json" % (hostName, viewID)

try:
	u = urlopen(url)
except HTTPError, e:
   print "The server at %s could not handle the request." % url
   print "Error code: ", e.code
except URLError, e:
   print "We failed to reach the server at %s." % url
   print "Reason: ", e.reason
else:
	response = load(u)
	
        pp = pprint.PrettyPrinter(indent=4)
	pp.pprint(response)
