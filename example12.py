#
# Example12.py - Shows code to access data in an API response
#
import json
import urllib2
import pprint
import time

# Get metadata for views in the Chicago data portal
fileHandle = urllib2.urlopen("http://data.cityofchicago.org/api/views.json")
views = json.load(fileHandle)

# 1 - Get the number of views that were returned
numViews = len(views)
print '\nNUMBER OF VIEWS RETURNED = %s\n' % numViews

# 2 - Access one of the metadata values.  Get the name of the first view.
viewName = views[0]['name']
print 'NAME OF FIRST VIEW = %s\n' % viewName

# 3 - Iterate through the views and print the name of each view
print 'NAMES OF ALL %s VIEWS DOWNLOADED:' % numViews
for view in views:
	print view['name']

# 4 - Print all metadata for first view, both the keys and values, including all nested pairs 
print '\nFORMATTED DUMP OF THE FIRST VIEW SHOWING ALL KEYS AND VALUES:'
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(views[0])

# 5 - Iterate thru first view and print the keys.  Does not print nested keys
print '\nHIGH-LEVEL FIELDS IN A VIEW:'
for key in views[0].iterkeys():
	print key

# 6 - Access a nested key-value pair.  Print the name of the view owner.
ownerName = views[0]['owner']['displayName']
print '\nNAME OF THE OWNER OF THE FIRST VIEW %s\n' % ownerName

# 7 - Get and print a time value.  It's in seconds since the epoch.  
secsOwnerProfileModified =  views[0]['owner']['profileLastModified']
print 'OWNER OF FIRST VIEW LAST MODIFIED HIS/HER USER PROFILE %s SECONDS SINCE JANUARY 1, 1970\n' % secsOwnerProfileModified

# 8 - Now print the time value in local timezone.
localtimeOwnerProfileModified = time.ctime(secsOwnerProfileModified)
print 'OWNER LAST MODIFIED HIS/HER USER PROFILE ON %s\n' %localtimeOwnerProfileModified
