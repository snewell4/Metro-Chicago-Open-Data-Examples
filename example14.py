from urllib2 import urlopen, URLError, HTTPError

# 1 - Good URL and service name
print '\nHere\'s what happens with a good URL.'
url = 'http://data.cityofchicago.org/api/views.json'
try:
   u = urlopen(url)
except HTTPError, e:
   print 'The server could not handle the request.'
   print 'Error code: ', e.code
except URLError, e:
   print 'We failed to reach a server.'
   print 'Reason: ', e.reason
else:
   print 'OK'

# 2 - Bad URL
print '\nHere\'s what happens with a bad URL.'
url = 'http://XYZ.cityofchicago.org/api/views.json'
try:
   u = urlopen(url)
except HTTPError, e:
   print 'The server could not handle the request.'
   print 'Error code: ', e.code
except URLError, e:
   print 'We failed to reach a server.'
   print 'Reason: ', e.reason
else:
   print 'OK'

# 3 - Bad service name
print '\nHere\'s what happens with a good URL but bad API service name.'
url = 'http://data.cityofchicago.org/api/XYZ.json'
try:
   u = urlopen(url)
except HTTPError, e:
   print 'The server could not handle the request.'
   print 'Error code: ', e.code
except URLError, e:
   print 'We failed to reach a server.'
   print 'Reason: ', e.reason
else:
   print 'OK'

# 4 - Bad parameter
print '\nHere\'s what happens with a good URL and good API service name but bad parameter.'
url = 'http://data.cityofchicago.org/api/views.json?XYZ=2'
try:
   u = urlopen(url)
except HTTPError, e:
   print 'The server could not handle the request.'
   print 'Error code: ', e.code
except URLError, e:
   print 'We failed to reach a server.'
   print 'Reason: ', e.reason
else:
   print 'OK'
print u.read()
