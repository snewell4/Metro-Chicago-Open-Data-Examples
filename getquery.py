#
#  getquery - Prints the query resource in a filtered view
#             This is used to quickly create the query document used in an INLINE filter API request.
#
#  args:      <hostname> <viewID>
#             If <hostname> is "-cook", use the Cook County Data Portal host name
#             If <hostname> is "-chicago", use the City of Chicago Data Portal host name
#             If <hostname> is "-ill", use the State of Illinois Data Portal host name
#             Other <hosthame> is the host name for the Socrata site.  Do not include "http://"
#             <viewID> is the 9 character Socrata view (aka dataset) ID.  Format is:  "cccc-cccc"
#
#  output:    The 'query' portion of the view metadata.  The unicode indicators are stripped off the strings.
#             The output is intended to be ready to be used in a program that is going to call the Socrata
#             views service API with an INLINE filter request.
#
import sys
from urllib2 import urlopen, URLError, HTTPError
from json import load
import pprint


hostNameChicago = "data.cityofchicago.org"
hostNameCook = "datacatalog.cookcountyil.gov"
hostNameIll = "data.illinois.gov"

if len(sys.argv) !=3:
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
url = "http://%s/api/views/%s/rows.json" % (hostName, viewID)

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

	pp = pprint.PrettyPrinter(indent=3)
	pp.pprint(response['meta']['view']['query'])


