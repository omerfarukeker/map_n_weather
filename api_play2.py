# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 21:44:49 2019
API PLAY 2
@author: omerzulal
"""

import requests
geocode_key = "PLACE YOUR GEOCODE KEY HERE"

#%% GETPLACE function returns the formatted address given the latitude and longitude
#using the google geocode api
def getplace(lat, lon):
    url = "https://maps.googleapis.com/maps/api/geocode/json?"
    url += "latlng=%s,%s&key=%s" % (lat, lon, geocode_key)
    j = requests.get(url).json()
    
    if j['results']:
        place = "{}".format(j['results'][-2]['formatted_address'])
        return place
    else:
        return 'Not Found'

#%% RETURN_TEMP function calculates the weather in Celsius and returns 
def return_temp(lat,lon):
    weather_apikey = "PLACE YOUR WEATHERMAP API KEY HERE"
    base_temp = r"https://api.openweathermap.org/data/2.5/weather?"
    url_temp = base_temp + "lat={}&lon={}&".format(lat,lon)
    url_temp += "appid={}&".format(weather_apikey)
    return requests.get(url_temp).json()["main"]["temp"] - 273.15

#%% GOOGLE MAPS API PART
import matplotlib.pyplot as plt
import numpy as np 
from PIL import Image
import matplotlib.animation as an

try:
    from StringIO import StringIO
except ImportError:
    from io import BytesIO as StringIO

plt.close('all')

#get one Google Static Map api key from google and use
static_api_key = "PLACE YOUR GOOGLE STATIC MAP API KEY HERE"
zoom = 7 # zoom level for the google map
mapsize = (700,700) # size of the snapshot from google map
maptypes = ["roadmap","satellite","terrain","hybrid"]
file_formats = ["png","png32","gif","jpg"]
base_url = 'https://maps.googleapis.com/maps/api/staticmap?'

# create random list of latitudes and longitudes
size = 20
lat = np.random.uniform(low=37, high=41, size=size)
lon = np.random.uniform(low=27, high=44, size=size)

address_list = []
fig = plt.figure(figsize=(7,7))
ax = fig.add_subplot(111)
gif_file= []
for i in range(size):
    address = getplace(lat[i], lon[i])
    temp = return_temp(lat[i], lon[i])
    print(address)
    address_list.append(str(address))
    
    url = base_url
    url += "center={},{}&".format(lat[i],lon[i])
    url += "zoom={}&".format(zoom)
    url += "size={}x{}&".format(mapsize[0],mapsize[1])
    url += 'maptype={}&'.format(maptypes[0])
    url += 'format={}&'.format(file_formats[1])
    url += 'key={}&'.format(static_api_key)
    url += "markers=color:green|label:|{},{}".format(lat[i],lon[i])
    
    r = requests.get(url)
    img = Image.open(StringIO((r.content)))

    gif_file.append([ax.imshow(np.array(img)), ax.text(180,270,str(address)+"\nTemperature: %.1f Celsius"%(temp),fontsize=12,fontweight='bold')])
    
delay = 900 #milliseconds
anim = an.ArtistAnimation(fig,gif_file,interval=delay)
anim.save("map_n_weather.gif")
