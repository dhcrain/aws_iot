import json
import urllib2
import os
import calendar
from datetime import datetime

google_map_api_key = os.environ["GOOGLE_MAPS_API_KEY"]
location = os.environ["TZ_LOCATION"]
current_timestamp_utc = calendar.timegm(datetime.utcnow().utctimetuple())


def call_api(url):
    response = urllib2.urlopen(url)
    return json.load(response)


time_url = "https://maps.googleapis.com/maps/api/timezone/json?location={}&timestamp={}&key={}".format(location, current_timestamp_utc, google_map_api_key)
time_data = call_api(time_url)
print(time_data['rawOffset'])
