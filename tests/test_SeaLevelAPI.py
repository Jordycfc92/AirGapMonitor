import sys
import os

correct_path = os.path.abspath('python')
print("Path being added to sys.path:", correct_path)
sys.path.append(correct_path)

import requests
import unittest
from unittest.mock import patch, MagicMock

from SeaLevelAPI import SeaLevelAPI
import arrow

class TestSeaLevelAPI(unittest.TestCase):
    def setUp(self):
        # Load a dummy environment file or set environment variables directly
        self.api = SeaLevelAPI('path/to/dummy/env')

    @patch('SeaLevelAPI.requests.get')
    def test_fetch_data(self, mock_get):
        # Set up the mock to return a successful response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'data': [{'time': '2024-04-18T12:00:00Z', 'sg': 1.2}]
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        
        # Call fetch_data
        result = self.api.fetch_data(43.38, -3.01, arrow.now(), arrow.now().shift(hours=8))
        
        # Assert call was made correctly
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        mock_get.assert_called_once()

    @patch('SeaLevelAPI.requests.get')
    def test_fetch_data_failure(self, mock_get):

        mock_get.side_effect = requests.exceptions.ConnectionError

        # Attempt to call fetch_data to trigger the connection error.
        with self.assertRaises(requests.exceptions.ConnectionError):  
            self.api.fetch_data(43.38, -3.01, arrow.now(), arrow.now().shift(hours=8))

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
