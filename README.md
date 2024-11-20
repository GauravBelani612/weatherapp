README.txt

Download all files to the same directory in order to run them from your terminal
Navigate to this directory in your terminal

Weather Application Instructions:

In your terminal, type "python3 weatherapp.py"
The help message should explain command options
-s, -a, and -r require 1 city as an argument
-u requires 2 cities as arguments
-l, -c, -h, and -e require no arguments.

Weather Application Unittest Instructions:

In your terminal, type "python3 -m unittest unittestweather.py"
The first test checks if latitude/longitude data is being accessed correctly for San Francisco, first fetching from the API and secondly accessing caches from coords dict.
The second test checks for behavior when a fake city "Gaurav" is searched
The third test checks if weather data is being accessed correctly using dummy data for Austin weather
If all three tests pass, it should say OK. If not, an assertion error will be raised.
