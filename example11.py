import urllib2
f = urllib2.urlopen("http://data.cityofchicago.org/api/views.json?count=true")
response = f.read()  
print response 
