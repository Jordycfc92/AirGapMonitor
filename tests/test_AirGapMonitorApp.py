
from tkinter import Tk
import unittest
from unittest.mock import patch
from GUI import AirGapMonitorApp  

class TestAirGapMonitorApp(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.app = AirGapMonitorApp(self.root)  # Updated instantiation

    def test_initialization(self):
        # Check if the main frame and widgets are set up
        self.assertIn('firstPage', self.app.frames)
        self.assertIsNotNone(self.app.frames['firstPage'])

    @patch('GUI.messagebox.showerror')  # Updated the location of patching
    def test_input_validation(self, mock_showerror):
        # Simulate entering invalid latitude and try fetching data
        self.app.latEntry.insert(0, 'invalid_latitude')
        self.app.fetch_data()
        # Check if error messagebox is shown
        mock_showerror.assert_called_once()

    def tearDown(self):
        self.root.destroy()

if __name__ == '__main__':
    unittest.main()
