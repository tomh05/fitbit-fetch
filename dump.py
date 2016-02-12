import fitbit
import ConfigParser
import json
import datetime
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

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

# while date less than ....

date_string = date_selected.strftime('%Y-%m-%d')

authd_client = fitbit.Fitbit(CI_id, CI_client_secret, oauth2=True, access_token=CI_access_token, refresh_token=CI_refresh_token)
 
#iterate over days

intra_steps = authd_client.intraday_time_series('activities/steps', base_date  = date_string , detail_level = '1min', start_time   = None, end_time     = None)
 
f = open( name + '_' + date_string+ '_' + 'steps.json', 'w')
json.dump(intra_steps, f)
f.close()
 
intra_heart = authd_client.intraday_time_series('activities/heart', base_date  = date_string , detail_level = '1sec', start_time   = None, end_time     = None)
 
f = open( name + '_' + date_string+ '_' + 'heart.json', 'w')
json.dump(intra_heart, f)
f.close()

sleep = authd_client.get_sleep(date_selected)
f = open( name + '_' + date_string+ '_' + 'sleep.json', 'w')
json.dump(sleep, f)
f.close()
