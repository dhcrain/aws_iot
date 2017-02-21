import calendar
import urllib2
import json
from datetime import datetime
import os

google_map_api_key = os.environ["GOOGLE_MAPS_API_KEY"]
start_address = os.environ["START_ADDRESS"]
end_address = os.environ["END_ADDRESS"]
current_time = calendar.timegm(datetime.utcnow().utctimetuple())

url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins={}&destinations={}&departure_time={}&traffic_model=pessimistic&units=imperial&key={}".format(start_address, end_address, current_time, google_map_api_key)
response = urllib2.urlopen(url)
data = json.load(response)

travel_time_sec = data['rows'][0]['elements'][0]['duration_in_traffic']['value']
arrival_time_unix = current_time + travel_time_sec + 120

arrival_time = datetime.fromtimestamp(arrival_time_unix).strftime("%I:%M %p %Z")
message = "Walking out, should get home by {}".format(arrival_time)
