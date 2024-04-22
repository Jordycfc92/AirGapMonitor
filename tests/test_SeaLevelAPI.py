
import unittest
from unittest.mock import patch, MagicMock

from SeaLevelAPI import SeaLevelAPI
import arrow

class TestSeaLevelAPI(unittest.TestCase):
    def setUp(self):
        # Load a dummy environment file or set environment variables directly
        self.api = SeaLevelAPI.SeaLevelAPI('path/to/dummy/env')

    @patch('seaLevelAPI.requests.get')
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

    @patch('seaLevelAPI.requests.get')
    def test_fetch_data_failure(self, mock_get):
        # Simulate a connection error
        mock_get.side_effect = SeaLevelAPI.requests.exceptions.ConnectionError()
        
        # Call fetch_data and handle exceptions
        with self.assertRaises(SeaLevelAPI.requests.exceptions.ConnectionError):
            self.api.fetch_data(43.38, -3.01, arrow.now(), arrow.now().shift(hours=8))

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
