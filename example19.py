#
#  rats   - Takes a Chicago street address as input and opens a map in your
#           default browser with nearby locations of rat complaints.  The
#           address is the center of a circle that is <radius> meters.  Rodent
#           baiting requests in that circle will appear on the map.  The total
#           number of rats found is printed in the command prompt window.
#
#           The maximum number of markers on the map is maxNumRatsInMap. If the
#           URL has too many markers, it becomes too long for Google and
#           generates and error.  Playing with this max keeps the URL short
#           enough to process.  If more rats than the max are found, the first
#           maxNumRatsInMap are displayed on map.  A message is printed to the
#           command prompt window informing user the number of rats in the map.
#
#           Uses Google Maps API for geocoding and map display.
#           Uses Chicago Data Portal 311 Service Requests for Rodent Baitig in
#           2011.
#           Does not check for duplicate complaints or open/closed complaints.
#
#  usage:   python rats.py <street> [radius]
#
#  example: python rats.py "2400 West Fullerton"
#           python rats.py "2400 w fullerton" 200
#
#  args:    <street> - street address in quotes.  Assumes city is Chicago and
#               state is IL
#           <radius> - find rat complaints in circle centered on <street> that is
#               <radius> meters in radius.  Default is 100.  Must be greater than 0.
# 
import httplib
import sys
import pprint
import json
import urllib
from urllib2 import Request, urlopen, URLError, HTTPError
import os


#
#   geocode(street, city, state) returns the latitude and longitude of a
#       street address using Google's map API.  Note, there is a limit on
#       the number of geocode requests you can make each day to Google.
#
#   Args:
#       street - string - street address
#       city - string - city name
#       state - string - state name
#
#   Returns:
#       err - string - error information.  If empty, geocode was successful
#       lat - string - latitude of the street address
#       lng - string - longitude of the street address
#
def geocode(street, city, state):
    err = ""
    lat = ""
    lng = ""
    url =  "http://maps.googleapis.com/maps/api/geocode/json?address=" + \
        urllib.quote_plus(street) + ',' + \
        urllib.quote_plus(city)   + ',' + \
        urllib.quote_plus(state)  + \
        "&sensor=false"
    req = Request(url)
    try:
	u = urlopen(req)
    except URLError, e:
        if hasattr(e, 'reason'):
            err = e.reason
	elif hasattr(e, 'code'):
            err = e.code
    else:
        response = json.load(u)
        # Check that Google sent back valid data.  If so, get lat and long.
        if response['status'] == 'OK':
            lat = response['results'][0]['geometry']['location']['lat']
            lng = response['results'][0]['geometry']['location']['lng']
        # otherwise, Google returned an error
        else:
            err = 'Google error code: %s\n' % response['status']
    return err, str(lat), str(lng)

#
#   getRatLocs(lat, lng, rad) returns a list of the locations of rats
#       from the Chicago 311 service requests for rodent baiting.  The
#       locations will be within the circle that has a center point at
#       lat/lon and a radius of rad meters.
#
#   Args:
#       lat - latitude of the center point of the circle
#       lng - longitude of the center point of the circle
#       rad - radius, in meters, of the circle
#
#   Returns:
#       err - string with error information.  If empty, geocode was successful
#       locs - a list with each item being a sublist containing two
#           elements: latitude and longitude that represents the location of
#           a rat baiting request.
#
def getRatLocs(lat, lng, rad):
    # parameters used in the SODA POST request to do the search
    hostName   = "data.cityofchicago.org"
    service    = "/views/INLINE/rows"
    formatType = "json"
    parameters = "method=index"
    headers    = { "Content-type:" : "application/json" }
    # SODA inline query.  Lat, Lng, Radius are set to 0 here.
    # columnId must match the ID in the view for the Location column
    query = {
        "originalViewId": "97t6-zrhs",
        "name": "Nearby rats",
        "query": {
            "filterCondition": {
                "type": "operator",
                "value": "within_circle",
                "children": 
                    [
                        {
                            "type": "column",
                            "columnId": 2849547
                        },
                        {
                            "type": "literal",
                            "value": 0
                        },
                        { 
                            "type": "literal",
                            "value":  0
                        },
                        {
                            "type": "literal",
                            "value": 0
                        }
                    ]
                }
            }
         }
    # constants used to index into inline filter children[]
    queryLat = 1
    queryLng = 2
    queryRad = 3
    # constants for table column numbers in query return data
    colNumLat = 22
    colNumLng = 23
    # constants used to index into locs
    locLat = 0
    locLng = 1

    # initialize return variables to be empty
    err = ''
    locs = list()

    # put lat, lng, radius into the inline query
    query["query"]["filterCondition"]["children"][queryLat]["value"] = lat
    query["query"]["filterCondition"]["children"][queryLng]["value"] = lng
    query["query"]["filterCondition"]["children"][queryRad]["value"] = rad
    # setup and send the inline query
    jsonQuery = json.dumps(query)
    request = service + '.' + formatType + '?' + parameters 
    conn = httplib.HTTPConnection(hostName)
    conn.request("POST", request, jsonQuery, headers)
    response = conn.getresponse()
    # check for good response, pull data out of response and setup locs
    if response.reason != 'OK':
        err = "%s %s" % (response.status, response.reason)
    else:
        rawResponse = response.read()
        jsonResponse = json.loads(rawResponse)
        for rowData in jsonResponse['data']:
            locs.append([rowData[colNumLat], rowData[colNumLng]])
    return err, locs


#
#   createMapUrl(centerLat, centerLng, locs) returns the URL for a Google
#       static map that has a marker for the center of the map and markers
#       for the locations in locs.
#
#   Args:
#       centerLat - string - latitude of the center point of the map
#       centerLng - string - longitude of the center point of the map
#       locs - list - where each item is a location to be marked on the map.
#           Each item is a sublist with two strings: latitude and longitude
#       n - integer - the first n locations in locs will be marked on the
#           map.  There is an upper limit on the size of the URL sent to
#           the Google Map API.  A long list of locations in the URL will
#           not be accepted.  n keeps the URL within the limit.
#
#   Returns:
#       URL - string - URL to send to the Google Map API to create a static
#           map in the default browser.
#
def createMapUrl(centerLat, centerLng, locs, n):
    # define constants for indexing into the locs sublist
    locLat = 0
    locLng = 1
    # define parameters for the map
    urlMapAPI = "http://maps.googleapis.com/maps/api/staticmap"
    mapZoomLevel = "14"
    mapHeight = "512"
    mapWidth = "512"
    mapType = "roadmap"
    centerMarkerColor = "blue"
    centerMarkerLabel = "C"
    locMarkerColor = "red"
    locMarkerLabel = "R"

    url = \
        urlMapAPI + '?' + \
        'center=' + centerLat + ',' + centerLng + \
        '&' + \
        'size=' + mapHeight + 'x' + mapWidth + \
        '&' + \
        'maptype=' + mapType + \
        '&' + \
        'sensor=false' + \
        '&' + \
        'markers=color:' + centerMarkerColor + '%7C' + \
        'label:' + centerMarkerLabel + '%7C' + centerLat + ',' + centerLng 

    i = 0
    for loc in locs:
        if i < n:
            url += '&' + \
                'markers=color:' + locMarkerColor + '%7C' + \
                'label:' + locMarkerLabel + '%7C' + \
                loc[locLat] + ',' + loc[locLng]
        i +=1
    return url



# constants used to index into addr[]
indexStreet = 0
indexCity = 1
indexState = 2
# defaults
circleRadius = 100    
maxNumRatsInMap = 20 

if len(sys.argv) < 2 or len(sys.argv) > 3:
    sys.stderr.write("Usage: python %s \"street\" [radius]\n" % sys.argv[0])
    raise SystemExit(1)

addr = sys.argv[1]

if len(sys.argv) == 3:
    try:
        circleRadius = int(sys.argv[2])
    except:
        sys.stderr.write("Usage: python %s \"street\" [radius]\n" % sys.argv[0])
        raise SystemExit(1)

if circleRadius <= 0:
    sys.stderr.write("Usage: python %s \"street\" [radius]\n" % sys.argv[0])
    raise SystemExit(1)

err, circleCenterLat, circleCenterLng = geocode(addr, 'Chicago', 'IL')
if (err != ""):
    print "Geocoding error = %s" % err
    sys.exit(0)

err, ratLocations = getRatLocs(circleCenterLat, circleCenterLng, circleRadius)
if (err != ""):
    print "Query error = %s" % err
    sys.exit(0)

url = createMapUrl(circleCenterLat, circleCenterLng, ratLocations, maxNumRatsInMap)

numRats = len(ratLocations)
print "%d rats!" % numRats
if numRats > maxNumRatsInMap :
    print "The map only displays the first %d rats.\n" % maxNumRatsInMap

os.startfile(url)

sys.exit(0)
