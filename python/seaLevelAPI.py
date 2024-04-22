from dotenv import load_dotenv
import os
import requests
import arrow
import json


class SeaLevelAPI:
    def __init__(self, envFile):
        load_dotenv(envFile)
        self.api_key = os.getenv("STORMGLASS_API_KEY")
        self.base_url = 'https://api.stormglass.io/v2/tide/sea-level/point'
        
        #Proving APIKey is correct
        #print("this is the api key" + self.api_key)

    
    def fetch_data(self, lat, lng, start, end):
        headers = {'Authorization': self.api_key}
        params = {
            'lat': lat,
            'lng': lng,
            'start': start.timestamp(),
            'end': end.timestamp(),
        }
        try:
            response = requests.get(self.base_url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.HTTPError as errhttp:
            print(f"Http Error: {errhttp}")
            
        except requests.exceptions.ConnectionError as errconnection:
            print(f"Connection Error: {errconnection}")
            
        except requests.exceptions.Timeout as errtimeout:
            print(f"Timeout Error: {errtimeout}")
            
        except requests.exceptions.RequestException as err:
            print(f"Unknown Error: {err}")
            


""" 

   def fetch_data(self, lat, lng, start, end):
        headers = {'Authorization': self.api_key}
        params = {
            'lat': lat,
            'lng': lng,
            'start': start.timestamp(),
            'end': end.timestamp(),
        }
        try:
            response = requests.get(self.base_url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.HTTPError as errhttp:
            print(f"Http Error: {errhttp}")
        except requests.exceptions.ConnectionError as errconnection:
            print(f"Connection Error: {errconnection}")
        except requests.exceptions.Timeout as errtimeout:
            print(f"Timeout Error: {errtimeout}")
        except requests.exceptions.RequestException as err:
            print(f"Unknown Error: {err}") 






fetch = SeaLevelAPI('exclude/config.env')
data = fetch.fetch_data(43.38, -3.01, arrow.now().floor('hour'), arrow.now().floor('hour').shift(hours=8))

for entry in data['data']:
    sg = entry["sg"]
    time = arrow.get(entry["time"])

    print(f"Time: {time.format('HH:mm')}, tide: {sg}")

#pretty_json = json.dumps(data, indent=4)
#print(pretty_json)  





"""