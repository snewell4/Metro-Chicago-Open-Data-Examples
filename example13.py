from urllib2 import urlopen
from json import load

# 1 - Ask for all views
url = 'http://data.cityofchicago.org/api/views.json'
u = urlopen(url)
views = load(u)
numViews = len(views)
print '\nAsk for all views.  Number of views returned = %s' % numViews
for view in views:
   print '   ', view['name']

# 2 - Ask for views with 'police' in the name
url = 'http://data.cityofchicago.org/api/views.json?name=police'
u = urlopen(url)
views = load(u)
numViews = len(views)
print '\nAsk for \"police\" in name.  Number of views returned = %s' % numViews
for view in views:
   print '   ', view['name']

# 3 - Ask for views with 'police station' in the name
url = 'http://data.cityofchicago.org/api/views.json?name=police+station'
u = urlopen(url)
views = load(u)
numViews = len(views)
print '\nAsk for \"police station\" in name.  Number of views returned = %s' % numViews
for view in views:
   print '   ', view['name']

# 4 - Ask for views with 'police' in the name but set a limit of just returning two views
url = 'http://data.cityofchicago.org/api/views.json?name=police&limit=2'
u = urlopen(url)
views = load(u)
numViews = len(views)
print '\nAsk for \"police\" in name and limit to two views.  Number of views returned = %s' % numViews
for view in views:
   print '   ', view['name']


