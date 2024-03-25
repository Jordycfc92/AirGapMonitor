import time
from lidar_lite import Lidar_Lite
import array as arr

class AirgapMonitor:
    def __init__(self, lidarBus=1, currentLidarAirgap = 0.0, currentCalculatedAirgap = 0.0, preHoldCondition = False, currentOperationHistory = [0]):
        self.lidarAirgap = currentLidarAirgap
        self.calculatedAirgap = currentCalculatedAirgap
        self.preHoldCondition = preHoldCondition
        self.history = currentOperationHistory
        self.lidar = Lidar_Lite()
        statusConnection = self.lidar.connect(lidarBus)

        #check connection
        if statusConnection == -1:
            print("Connection not established to sensor")
        else:
            print("Lidar sensor connection established")



    def setLegLength(self):
        try:
            user_input = float(input("Please enter leg 2 length: "))
            if 1.8 <= user_input <= 85.0:
                print(f"You entered: {user_input} ")
                return user_input
            else:
                print("The input was outside the boundary of 1.8m and 85.0m")
                return -1
        except ValueError:
            print("Invalid value entered, please try again")
            return None

    def lidarAirgap(self, ):
        # method to measure distance every one second whilst the jack-up is in a pre-hold
        while self.preHoldCondition:
            try:
                distance = self.lidar.getDistance()
                AirgapMonitor.currentLidarAirgap = distance
                print(f"Current airgap distance: {distance} cm")

            except Exception as e:
                print(f"An error occurred whilst getting the measurement {e}")

            #for sake of number of measurments one per second is the starting figure 
                time.sleep(1)