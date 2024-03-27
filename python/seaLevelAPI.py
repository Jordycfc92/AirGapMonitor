import requests

class SeaLevelAPI:
    BASE_URL = 'https://api.stormglass.io/v2/tide/sea-level/point'

    def __init__(self, apiKey):
        self.apiKey = apiKey

    def fetch_sea_level_data(self, lat, lng, start, end):
        headers = {'Authorization': self.apiKey}
        params = {
            'lat': lat,
            'lng': lng,
            'start': start.to('UTC').timestamp(),
            'end': end.to('UTC').timestamp(),
        }
        response = requests.get(self.BASE_URL, params=params, headers=headers)
        response.raiseForStatus()  # Raises an error for bad responses
        return response.json()
