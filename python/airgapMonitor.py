import time
from lidar_lite import Lidar_Lite
import array as arr

class AirgapMonitor:
    def __init__(self, lidarBus=1, currentLidarAirgap = 0.0, currentCalculatedAirgap = 0.0, preHoldCondition = False, currentOperationHistory = [0], currentLeg1length =0, currentLeg1Pen =0):
        self.lidarAirgap = currentLidarAirgap
        self.calculatedAirgap = currentCalculatedAirgap
        self.leg1length = currentLeg1length
        self.leg1Penetration = currentLeg1Pen
        self.preHoldCondition = preHoldCondition
        self.history = currentOperationHistory
        self.lidar = Lidar_Lite()
        statusConnection = self.lidar.connect(lidarBus)

        #check connection to lidar sensor
        if statusConnection == -1:
            print("Connection not established to sensor")
        else:
            print("Lidar sensor connection established")



    def setLeg1Length(self):
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
        
    def setLeg1Penetration(self):
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

    def monitorLidarAirgap(self, ):
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

    def monitorCalculatedAirgap(self, ):
        #airgaps are calculated by leg length - (water depth + leg penetration)
        #water depth is calculated by lowest astronomical tide (LAT) + tide 
        #leg penetration is calculated at zero airgap (ZAG) by leg length - water depth

        totalWaterDepth = 10 # this will be from an API call 
        self.calculatedAirgap = self.leg1length - (totalWaterDepth + self.leg1Penetration)

         

    def showCurrentAirgapAverage (self,):
        pass

    def showOperationReport(self):
        pass
