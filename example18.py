import os, urllib

urlMapAPI = "http://maps.googleapis.com/maps/api/staticmap"
mapCenterLat = "41.9249"
mapCenterLong = "-87.6876"
mapZoomLevel = "14"
mapHeight = "512"
mapWidth = "512"
mapType = "roadmap"
centerMarkerColor = "blue"
centerMarkerLabel = "C"
mapMarkerColor = "green"
mapMarkerLabel = "P"
mapMarkerLat = "41.9240"
mapMarkerLong = "-87.6876"


url = \
    urlMapAPI + '?' + \
    'center=' + mapCenterLat + ',' + mapCenterLong + \
    '&' + \
    'size=' + mapHeight + 'x' + mapWidth + \
    '&' + \
    'maptype=' + mapType + \
    '&' + \
    'sensor=false' + \
    '&' + \
    'markers=color:' + centerMarkerColor + '%7C' + 'label:' + centerMarkerLabel + '%7C' + mapCenterLat + ',' + mapCenterLong + \
    '&' + \
    'markers=color:' + mapMarkerColor + '%7C' + 'label:' + mapMarkerLabel + '%7C' + mapMarkerLat + ',' + mapMarkerLong 

os.startfile(url)



