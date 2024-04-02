import time
from lidar_lite import Lidar_Lite
import array as arr
import SeaLevelAPI
import arrow

class AirgapMonitor:
    def __init__(self, lidarBus=1, retries=5, backoff_factor=2, currentLidarAirgap = 0.0, currentCalculatedAirgap = 0.0, preHoldCondition = False, currentOperationHistory = [0], currentLeg1length =0, currentLeg1Pen =0):
        self.lidarAirgap = currentLidarAirgap
        self.calculatedAirgap = currentCalculatedAirgap
        self.leg1length = currentLeg1length
        self.leg1Penetration = currentLeg1Pen
        self.preHoldCondition = preHoldCondition
        self.history = currentOperationHistory
        self.retries = retries
        self.backoff_factor = backoff_factor
        self.lidar = Lidar_Lite()
        self.connect_with_retry(lidarBus)
        self.seaLevelAPI = SeaLevelAPI('exclude/config.env') # instance of sealevelAPI
        

    def connect_with_retry(self, lidarBus):
        attempt = 0
        while attempt < self.retries:
            print(f"Attempt {attempt + 1} to connect to the LiDAR sensor.")
            statusConnection = self.lidar.connect(lidarBus)
            
            if statusConnection == 0:
                print("Lidar sensor connection established.")
                return True
            else:
                print("Connection not established, retrying...")
                time.sleep((2 ** attempt) * self.backoff_factor)
                attempt += 1
        
            print("Failed to establish a connection after several attempts.")
            return False



    def set_leg1_length(self):
        try:
            user_input = float(input("Please enter leg 1 length: "))
            if 1.8 <= user_input <= 85.0:
                print(f"You entered: {user_input} ")
                self.leg1length = user_input
                return self.leg1length
            else:
                print("The input was outside the boundary of 1.8m and 85.0m leg length.")
                return None
        except ValueError:
            print("Invalid value entered, please try again")
            return None
        
    def set_leg1_penetration(self):
        try:
            user_input = float(input("Please enter leg 1 penetration: "))
            if 0 <= user_input <= 30.0:
                print(f"You entered: {user_input} ")
                self.leg1Penetration = user_input
                return self.leg1Penetration
            else:
                print("The input was outside the boundary of 0.0m and 30.0m of penetration.")
                return None
        except ValueError:
            print("Invalid value entered, please try again")
            return None

    def monitor_lidar_airgap(self, ):
        # method to measure distance every one second whilst the jack-up is in a pre-hold
        while self.preHoldCondition:
            try:
                distance = (self.lidar.getDistance())/10 #added to modify cm to m
                AirgapMonitor.currentLidarAirgap = distance
                print(f"Current airgap distance: {distance} cm")
                self.history.append(distance)

            except Exception as e:
                print(f"An error occurred whilst getting the measurement {e}")

            #for sake of number of measurments one per second is the starting figure 
                time.sleep(1)

    def monitor_calculated_airgap(self, lat, lng, lowest_tide):
            # latitude and longitude are provided for the sea level API call
            totalWaterDepth = (self.self.collect_tide_data(lat, lng)) - lowest_tide
            if totalWaterDepth is not None:
                self.calculatedAirgap = self.leg1length - (totalWaterDepth + self.leg1Penetration)
            else:
                print("Failed to fetch sea level data for airgap calculation.")

    
    def collect_tide_data(self, lat, lng):
        # current sea level
        now = arrow.now()
        data = self.seaLevelAPI.fetch_data(lat, lng, now, now.shift(hours=4))  # Fetch data for the next hour
        if data and 'data' in data and len(data['data']) > 0:
            # (sg) from the first entry
            return data['data'][0]['sg']
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
