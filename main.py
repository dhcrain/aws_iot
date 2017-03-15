

from __future__ import print_function

import boto3
import json
import logging
import os
import calendar
import urllib2
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

sns = boto3.client('sns', region_name='us-west-2')
# sns = boto3.client('sns')
phone_number = os.environ["PHONE_NUMBER"]
google_map_api_key = os.environ["GOOGLE_MAPS_API_KEY"]
start_address = os.environ["START_ADDRESS"]
end_address = os.environ["END_ADDRESS"]
tz_location = os.environ["TZ_LOCATION"]
walk_from_desk_to_car = 180
current_timestamp_utc = calendar.timegm(datetime.utcnow().utctimetuple())


def call_api(url):
    response = urllib2.urlopen(url)
    return json.load(response)


time_url = "https://maps.googleapis.com/maps/api/timezone/json?location={}&timestamp={}&key={}".format(tz_location, current_timestamp_utc, google_map_api_key)
time_offset = call_api(time_url)['rawOffset']

travel_url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins={}&destinations={}&departure_time={}&traffic_model=pessimistic&units=imperial&key={}".format(start_address, end_address, current_timestamp_utc, google_map_api_key)
travel_time_sec = call_api(travel_url)['rows'][0]['elements'][0]['duration_in_traffic']['value']
arrival_time_unix = (current_timestamp_utc + travel_time_sec + time_offset + walk_from_desk_to_car)
arrival_time = datetime.fromtimestamp(arrival_time_unix).strftime("%I:%M %p %Z")


def lambda_handler(event, context):
    logger.info('Received event: ' + json.dumps(event))
    message = "Walking out, should get home by {}".format(arrival_time)
    sns.publish(PhoneNumber=phone_number, Message=message)
    logger.info('SMS has been sent to ' + phone_number + message)
