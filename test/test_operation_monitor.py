import unittest
from unittest.mock import patch
from OperationMonitor import OperationMonitor

class TestOperationMonitor(unittest.TestCase):

    def setUp(self):
        self.op_monitor = OperationMonitor()

    @patch('lidar_lite.Lidar_Lite.connect')
    def test_lidar_connection_success(self, mock_connect):
        # Simulate successful connection
        mock_connect.return_value = 0  
        self.assertTrue(self.op_monitor.connect_with_retry(1))

    @patch('lidar_lite.Lidar_Lite.connect')
    def test_lidar_connection_failure(self, mock_connect):
        # Simulate failed connection
        mock_connect.return_value = -1  
        self.assertFalse(self.op_monitor.connect_with_retry(1))

    @patch('OperationMonitor.OperationMonitor.collect_tide_data')
    def test_calculated_airgap(self, mock_collect_tide_data):
        mock_collect_tide_data.return_value = [("2023-04-20T10:00:00", 3.5)]
        self.op_monitor.lowesttide = 2.0
        self.op_monitor.leg1length = 10
        self.op_monitor.leg1Penetration = 1.5
        expected_airgap = 10 - (3.5 + 2.0 + 1.5)  # leg1length - (sg + lowesttide + leg1Penetration)
        self.assertEqual(self.op_monitor.monitor_calculated_airgap(1, 1, 2.0), expected_airgap)


if __name__ == '__main__':
    unittest.main()
