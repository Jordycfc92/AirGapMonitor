import sys
sys.path.append('/Users/jordanmcmillan/VSCode/AirGapMonitor/python')
import unittest
from unittest.mock import patch, Mock

import requests
from SeaLevelAPI import SeaLevelAPI


class TestSeaLevelAPI(unittest.TestCase):

    @patch('requests.get')
    def test_fetch_data_success(self, mock_get):
        # Mocking the response from requests
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": [{"time": "2023-04-20T12:00:00", "sg": 3.2}]}
        mock_get.return_value = mock_response

        api = SeaLevelAPI('exclude/config.env')
        data = api.fetch_data(1, 1, "2023-04-20T10:00:00", "2023-04-20T14:00:00")
        self.assertIn("data", data)
        self.assertEqual(data["data"][0]["sg"], 3.2)

    @patch('requests.get')
    def test_fetch_data_failure(self, mock_get):
        mock_get.side_effect = requests.exceptions.ConnectionError()
        api = SeaLevelAPI('exclude/config.env')
        with self.assertRaises(requests.exceptions.ConnectionError):
            api.fetch_data(1, 1, "2023-04-20T10:00:00", "2023-04-20T14:00:00")

if __name__ == '__main__':
    unittest.main()
