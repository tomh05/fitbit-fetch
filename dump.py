import fitbit
import ConfigParser
import json
import datetime
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()


def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)

#Load Settings
parser = ConfigParser.SafeConfigParser()
 
parser.read('config.ini')
 
CI_id              = parser.get('Login Parameters', 'CLIENT_ID')
CI_client_secret   = parser.get('Login Parameters', 'CLIENT_SECRET')
CI_access_token    = parser.get('Login Parameters', 'ACCESS_TOKEN')
CI_refresh_token   = parser.get('Login Parameters', 'REFRESH_TOKEN')
 
name              = parser.get('Storage Parameters', 'NAME')
start_date_string  = parser.get('Storage Parameters', 'START_DATE')
end_date_string    = parser.get('Storage Parameters', 'END_DATE')

# Parse date
start_date = datetime.datetime.strptime(start_date_string, "%Y-%m-%d").date()
end_date = datetime.datetime.strptime(end_date_string, "%Y-%m-%d").date()

date_selected = start_date

for date_selected in daterange(start_date, end_date):
  date_string = date_selected.strftime('%Y-%m-%d')
  authd_client = fitbit.Fitbit(CI_id, CI_client_secret, oauth2=True, access_token=CI_access_token, refresh_token=CI_refresh_token)
 
  #iterate over days

  activities = authd_client.activities(date  = date_string)
 
  f = open( name + '_' + date_string+ '_' + 'activities.json', 'w')
  json.dump(activities, f)
  f.close()

  # Steps
  intra_steps = authd_client.intraday_time_series('activities/steps', base_date  = date_string , detail_level = '1min', start_time   = None, end_time     = None)
 
  f = open( name + '_' + date_string+ '_' + 'steps.json', 'w')
  json.dump(intra_steps, f)
  f.close()

  f_csv = open( name + '_steps.csv', 'a')
  for entry in intra_steps["activities-steps-intraday"]["dataset"]:
    timestamp = date_string + " " + entry["time"] + " UTC"
    f_csv.write(name + ",steps,"+ timestamp + "," + str(entry["value"])+"\n")
  f_csv.close()


  # Calories
  intra_calories = authd_client.intraday_time_series('activities/calories', base_date  = date_string , detail_level = '1min', start_time   = None, end_time     = None)
 
  f = open( name + '_' + date_string+ '_' + 'calories.json', 'w')
  json.dump(intra_calories, f)
  f.close()

  f_csv = open( name + '_calories.csv', 'a')
  for entry in intra_calories["activities-calories-intraday"]["dataset"]:
    timestamp = date_string + " " + entry["time"] + " UTC"
    f_csv.write(name + ",calories,"+ timestamp + "," + str(entry["value"])+"\n")
  f_csv.close()
 

  # Distance
  intra_distance = authd_client.intraday_time_series('activities/distance', base_date  = date_string , detail_level = '1min', start_time   = None, end_time     = None)
 
  f = open( name + '_' + date_string+ '_' + 'distance.json', 'w')
  json.dump(intra_distance, f)
  f.close()

  f_csv = open( name + '_distance.csv', 'a')
  for entry in intra_distance["activities-distance-intraday"]["dataset"]:
    timestamp = date_string + " " + entry["time"] + " UTC"
    f_csv.write(name + ",distance,"+ timestamp + "," + str(entry["value"])+"\n")
  f_csv.close()
 

  # Floors
  intra_floors = authd_client.intraday_time_series('activities/floors', base_date  = date_string , detail_level = '1min', start_time   = None, end_time     = None)
 
  f = open( name + '_' + date_string+ '_' + 'floors.json', 'w')
  json.dump(intra_floors, f)
  f.close()
  f_csv = open( name + '_floors.csv', 'a')
  for entry in intra_floors["activities-floors-intraday"]["dataset"]:
    timestamp = date_string + " " + entry["time"] + " UTC"
    f_csv.write(name + ",floors,"+ timestamp + "," + str(entry["value"])+"\n")
  f_csv.close()


 

  # Elevation
  intra_elevation = authd_client.intraday_time_series('activities/elevation', base_date  = date_string , detail_level = '1min', start_time   = None, end_time     = None)
 
  f = open( name + '_' + date_string+ '_' + 'elevation.json', 'w')
  json.dump(intra_elevation, f)
  f.close()
  f_csv = open( name + '_elevation.csv', 'a')
  for entry in intra_elevation["activities-elevation-intraday"]["dataset"]:
    timestamp = date_string + " " + entry["time"] + " UTC"
    f_csv.write(name + ",elevation,"+ timestamp + "," + str(entry["value"])+"\n")
  f_csv.close()

 
  # Heart
  print "intra heart for day " + date_string 
  intra_heart = authd_client.intraday_time_series('activities/heart', base_date  = date_string , detail_level = '1sec', start_time   = None, end_time     = None)
 
  f = open( name + '_' + date_string+ '_' + 'heart.json', 'w')
  json.dump(intra_heart, f)
  f.close()

  f_csv = open( name + '_heart.csv', 'a')
  for entry in intra_heart["activities-heart-intraday"]["dataset"]:
    timestamp = date_string + " " + entry["time"] + " UTC"
    f_csv.write(name + ",heart,"+ timestamp + "," + str(entry["value"])+"\n")
  f_csv.close()

  sleep = authd_client.get_sleep(date_selected)
  f = open( name + '_' + date_string+ '_' + 'sleep.json', 'w')
  json.dump(sleep, f)
  f.close()
  f_csv = open( name + '_sleep.csv', 'a')
  for a_sleep in sleep["sleep"]:
    for entry in a_sleep["minuteData"]:
      timestamp = date_string + " " + entry["dateTime"] + " UTC"
      f_csv.write(name + ",sleep,"+ timestamp + "," + str(entry["value"])+"\n")
  f_csv.close()
