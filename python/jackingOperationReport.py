import json
import OperationMonitor
class JackingOperationReport:
    def __init__(self) -> None:
        self.opsMonitor = OperationMonitor.OperationMonitor()


    def save_to_json(self, data, file_name):
        """
        Save data to a JSON file.

        Parameters:
        data (dict): The data to save.
        file_name (str): The name of the file to save the data to.
        """
        try:
            with open(file_name, 'w') as json_file:
                json.dump(data, json_file, indent=4)
        except IOError as e:
            print(f"An error occurred while writing to the file: {e}")

    def get_lidar_data(self):
        return self.opsMonitor.history

    def main(self):
        """
        Main function to collect user input, read sensor data, generate random floats,
        and save them all to a JSON file.
        """
        lidar_data = self.get_lidar_data()

        # Prepare the complete data structure
        data = {
            "Lidar airgap": lidar_data,

        }

        # Save the data to a JSON file
        self.save_to_json(data, 'report.json')

if __name__ == "__main__":
    report = JackingOperationReport()
    report.main()