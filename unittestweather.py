import unittest
import weatherapp
from unittest.mock import patch

class TestWeatherApp(unittest.TestCase):

    @patch('requests.get')
    def test_get_latlon_caching(self, mock_get):
        coords = {}
        # Mock response for API call
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{"lat": 37.7749, "lon": -122.4194}]

        # Call the function for the first time
        latlon = weatherapp.get_latlon("San Francisco", coords)
        self.assertEqual(latlon, [37.7749, -122.4194])
        self.assertIn("San Francisco", coords)
        self.assertEqual(coords["San Francisco"], [37.7749, -122.4194])

        # Call the function again, no API call should be made
        mock_get.reset_mock()  # Clear previous mock call records
        latlon_cached = weatherapp.get_latlon("San Francisco", coords)
        self.assertEqual(latlon_cached, [37.7749, -122.4194])
        mock_get.assert_not_called()  # Ensure no new API calls were made

    @patch('requests.get')
    def test_invalid_city(self, mock_get):
        coords = {}
        # Mock response for invalid city
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = []

        # Call the function with an invalid city
        latlon = weatherapp.get_latlon("Gaurav", coords)
        self.assertEqual(latlon, (None, None))
        self.assertNotIn("Gaurav", coords)  # Ensure it's not cached

    @patch('requests.get')
    def test_get_weather(self, mock_get):
        coords = {"Austin": [30.2672, -97.7431]}
        # Mock response for weather API
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "current": {
                "temp": 75.0,
                "feels_like": 73.0,
                "weather": [{"main": "Clear", "description": "clear sky"}],
                "wind_speed": 5.0,
                "wind_deg": 180
            }
        }

        # Call the function and validate results
        weather = weatherapp.get_weather("Austin", coords)
        self.assertIsNotNone(weather)
        self.assertEqual(weather["current"]["temp"], 75.0)
        self.assertEqual(weather["current"]["weather"][0]["main"], "Clear")
        self.assertEqual(weather["current"]["weather"][0]["description"], "clear sky")
        self.assertEqual(weather["current"]["wind_speed"], 5.0)
        self.assertEqual(weather["current"]["wind_deg"], 180)


