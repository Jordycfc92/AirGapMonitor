import time
from lidar_lite import Lidar_Lite
import array as arr
from SeaLevelAPI import SeaLevelAPI
import arrow

class OperationMonitor:
    def __init__(self, lidarBus=1, retries=5, backoff_factor=2, currentLidarAirgap = 0.0, lat = 1, long = 1, lowest_tide = 1, currentCalculatedAirgap = 0.0, preHoldCondition = False, currentOperationHistory = [0], currentLeg1length =1.8, currentLeg1Pen =0.0):
        self.lidarAirgap = currentLidarAirgap
        self.calculatedAirgap = currentCalculatedAirgap
        self.latitude = lat
        self.longitude = long
        self.lowesttide = lowest_tide
        self.leg1length = currentLeg1length
        self.leg1Penetration = currentLeg1Pen
        self.preHoldCondition = preHoldCondition
        self.history = currentOperationHistory
        self.retries = retries
        self.currentLidarAirgap = currentLidarAirgap
        self.backoff_factor = backoff_factor
        self.lidar = Lidar_Lite()
        self.connect_with_retry(lidarBus)
        self.seaLevelAPI = SeaLevelAPI('exclude/config.env') # instance of sealevelAPI
        

    def connect_with_retry(self, lidarBus):
        attempt = 0
        while attempt < self.retries:
            print(f"Attempt {attempt + 1} to connect to the LiDAR sensor.")
            if self.lidar.connect(lidarBus) == 0:
                print("Lidar sensor connection established.")
                return True
            else:
                print("Connection not established, retrying...")
                time.sleep((2 ** attempt) * self.backoff_factor)
                attempt += 1

        print("Failed to establish a connection after several attempts.")
        return False


    def monitor_lidar_airgap(self):
        if not self.preHoldCondition:
            return  # Exit if not in pre-hold condition

        try:
            distance = self.lidar.getDistance() / 100  # Convert mm to m. This is using the third party lidar code to get a distance for the sensor
            if distance == 0.01:
                raise Exception('The value of distance was not captured')
            self.currentLidarAirgap = (distance - 25.0) # *** offset for sensor locations here *** currently 25m above bottom of hull
            print(f"Current airgap distance: {distance} m")
            self.history.append(distance)
        except Exception as e:
            print(f"An error occurred whilst getting the measurement: {e}")

    def monitor_calculated_airgap(self, lat, lng, lowest_tide):
        # latitude and longitude are provided for the sea level API call
        # Changed the collect_tide_data to return a list of tuples for populating tide table on GUI page
        # Implemented check for data and then taking first tuple for sg to work out airgap 
        
        # ***Think about implications for updating the tide table throughout the operation ***
        tide_data = self.collect_tide_data(lat, lng)
    
        # Check to avoid error crashing
        if tide_data:
            # Use only the first sg value from the list
            first_sg = tide_data[0][1] 
            totalWaterDepth = first_sg + lowest_tide
        
            calculatedAirgap = self.leg1length - (totalWaterDepth + self.leg1Penetration)
            return calculatedAirgap
        else:
            print("Failed to fetch sea level data for airgap calculation.")
            return None 

    
    def collect_tide_data(self, lat, lng):
        # current tide range from this hour for the next 4 hours
        now = arrow.now()
        data = self.seaLevelAPI.fetch_data(lat, lng, now, now.shift(hours=4))  # *** Adjust time frame for tide from here
        tide_data =[]
        if data and 'data' in data and len(data['data']) > 0:
            for entry in data['data']:
                time = arrow.get(entry["time"]).format('HH:mm')  # Format time for display
                sg = entry["sg"]
                tide_data.append((time, sg))
            return tide_data
        else:
            return None
         

    def show_current_airgap_average (self,):
        #average taken over five minutes, one measurement per second > 60*5
        if len(self.history) < 300:
            print("Not enough data for a 5-minute average.")
            return

        five_minute_average = sum(self.history[-300:]) / 300
        print(f"5-minute average airgap distance: {five_minute_average} cm")

    def show_operation_report(self):
        pass
