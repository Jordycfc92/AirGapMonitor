import sys
import os

correct_path = os.path.abspath('python')
print("Path being added to sys.path:", correct_path)
sys.path.append(correct_path)


import unittest
from unittest.mock import MagicMock, patch
from OperationMonitor import OperationMonitor

class TestOperationMonitor(unittest.TestCase):

    def setUp(self):
        # No instantiation here to prevent premature connection attempts
        pass

    @patch('OperationMonitor.Lidar_Lite')
    @patch('OperationMonitor.SeaLevelAPI')
    @patch('OperationMonitor.time.sleep', return_value=None)  # Mock sleep to speed up the test
    def test_init(self, mock_sleep, MockSeaLevelAPI, MockLidarLite):
        mock_lidar = MockLidarLite.return_value
        mock_lidar.connect.return_value = 0
        monitor = OperationMonitor(lidarBus=1)
        self.assertIsInstance(monitor.lidar, MagicMock)
        self.assertIsInstance(monitor.seaLevelAPI, MagicMock)
        print("Tests complete for test_init")

    @patch('OperationMonitor.Lidar_Lite')
    @patch('OperationMonitor.SeaLevelAPI')
    @patch('OperationMonitor.time.sleep', return_value=None)
    def test_connect_with_retry_success(self, mock_sleep, MockSeaLevelAPI, MockLidarLite):
        mock_lidar = MockLidarLite.return_value
        mock_lidar.connect.return_value = 0
        monitor = OperationMonitor(lidarBus=1)
        result = monitor.connect_with_retry(1)
        self.assertTrue(result)
        mock_lidar.connect.assert_called_once_with(1)

    @patch('OperationMonitor.Lidar_Lite')
    @patch('OperationMonitor.SeaLevelAPI')
    def test_connect_with_retry_failure(self, MockSeaLevelAPI, MockLidarLite):
        # Configure the mock to simulate connection failures
        mock_lidar = MockLidarLite.return_value
        mock_lidar.connect.return_value = -1  # Ensure it always fails

        # Instantiate OperationMonitor
        monitor = OperationMonitor(lidarBus=1)

        # Manually call connect_with_retry to control test flow
        result = monitor.connect_with_retry(1)
        
        # Assert that the connection attempt fails
        self.assertFalse(result)
        # Assert the connect method is called exactly `retries` times
        self.assertEqual(mock_lidar.connect.call_count, monitor.retries,
                         f"Expected {monitor.retries} calls, got {mock_lidar.connect.call_count}")



if __name__ == '__main__':
    unittest.main()