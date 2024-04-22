import unittest
from unittest.mock import MagicMock, patch
import OperationMonitor

class TestOperationMonitor(unittest.TestCase):
    def setUp(self):
        self.monitor = OperationMonitor.OperationMonitor()

    @patch('OperationMonitor.Lidar_Lite')
    def test_lidar_connection(self, mock_lidar):
        # Simulate successful connection on the second try
        mock_lidar_instance = mock_lidar.return_value
        mock_lidar_instance.connect.side_effect = [1, 0]  # 1: failure, 0: success
        result = self.monitor.connect_with_retry(lidarBus=1)
        self.assertTrue(result)
        self.assertEqual(mock_lidar_instance.connect.call_count, 2)

    @patch('OperationMonitor.Lidar_Lite')
    def test_lidar_connection_failure(self, mock_lidar):
        # Simulate repeated connection failures
        mock_lidar_instance = mock_lidar.return_value
        mock_lidar_instance.connect.return_value = 1  # Always fail
        result = self.monitor.connect_with_retry(lidarBus=1)
        self.assertFalse(result)
        self.assertEqual(mock_lidar_instance.connect.call_count, self.monitor.retries)

    @patch('OperationMonitor.SeaLevelAPI')
    def test_fetch_sea_level_data(self, mock_sealevelapi):
        # Mock SeaLevelAPI to return specific data
        mock_api_instance = mock_sealevelapi.return_value
        mock_api_instance.fetch_data.return_value = {
            'data': [{'time': '2024-04-18T12:00:00Z', 'sg': 1.2}]
        }
        data = self.monitor.collect_tide_data(1, 1)
        self.assertIsNotNone(data)
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
