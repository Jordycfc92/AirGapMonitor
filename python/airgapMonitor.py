from lidar_lite import Lidar_Lite
import array as arr

class AirgapMonitor:
    def __init__(self, currentLidarAirgap = 0.0, currentCalculatedAirgap = 0.0, preHoldCondition = False,currentOperationHistory = [0]  ):
        self.lidarAirgap = currentLidarAirgap
        self.calculatedAirgap = currentCalculatedAirgap
        self.preHoldCondition = preHoldCondition
        self.history = currentOperationHistory


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




    
    







