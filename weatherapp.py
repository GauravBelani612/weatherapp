import argparse
import requests
import shlex

def create_parser():
    """Creates the command-line parser with various arguments.

    Returns:
        argparse.ArgumentParser: The parser object with all commands initialized.
    """
    parser = argparse.ArgumentParser(description="Weather Application \n\nNote: Use quotes when handling cities with more than one word (e.g., \"San Francisco\").\n", formatter_class=argparse.RawTextHelpFormatter, add_help=False)
    parser.add_argument("-s", "--search", metavar="", help="Search for the weather details of a city")
    parser.add_argument("-a", "--add", metavar="", help="Add a city to favorites")
    parser.add_argument("-l", "--list", action="store_true", help="List all favorites")
    parser.add_argument("-r", "--remove", metavar="", help="Remove a city from favorites")
    parser.add_argument("-u", "--update", nargs=2, metavar="", help="Deletes city 1 from favorites and replaces it with city 2 (Two Arguments)")
    parser.add_argument("-c", "--clear", action="store_true", help="Clears all cities from favorites")
    parser.add_argument("-h", "--help", action="store_true", help="Shows this help message")
    parser.add_argument("-e", "--exit", action="store_true", help="Exit the weather app")
    return parser

def get_latlon(city, coords): 
    """Fetches the latitude and longitude of a given city.

    Args:
        city (str): The name of the city.
        coords (dict): City/Coordinate Pairs

    Returns:
        list: A list containing the latitude and longitude of the city.
        tuple: (None, None) if the city cannot be found.
    """

    if city in coords: #stores coordinates in dict so each city is only called once with the API
        return coords[city]
    
    url = f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid=711cd06ee69d38fdb723763e99a44032'

    try:
        response = requests.get(url)

        if response.status_code == 200:
            posts = response.json()
        else:
            print('Error:', response.status_code)
    except requests.exceptions.RequestException as e:
        print("Error: ", e)
    
    if posts:
        latlong = [posts[0]["lat"], posts[0]["lon"]]
        coords[city] = latlong
        return latlong
    else:
        print(f'Cannot find the city {city}.')
    return (None, None)

def get_weather(city, coords): 
    """Fetches the weather details of a given city.

    Args:
        city (str): The name of the city.
        coords (dict): City/Coordinate pairs

    Returns:
        dict: The weather details for the city.
        None: If the city or weather data cannot be found.
    """

    lat, lon = get_latlon(city, coords)
    if lat != None:

        url = f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly,daily,alert&units=imperial&appid=711cd06ee69d38fdb723763e99a44032'

        try: 
            response = requests.get(url)
            if response.status_code == 200:
                posts = response.json()
            else:
                print('Error:', response.status_code)
        except requests.exceptions.RequestException as e:
            print("Error: ", e)
        if posts:
            weather_details = posts
            return weather_details
        else:
            print(f"Cannot find the city {city}")
        return None
    return None

def print_weather(city, coords): 
    """Displays the weather details of a given city in a readable format.

    Args:
        city (str): The name of the city.
        coords (dict): City/Coordinate pairs
    """
    weather = get_weather(city, coords)
    if weather != None:
        print(f"City Name: {city}") #prints city name
        temp = weather["current"]["temp"]
        print("Current Temperature: " + str(temp) + chr(176) + "F/" + str(round((temp - 32)*5/9, 2)) + chr(176) + "C") #prints current temperature in Farenheit and Celcius
        feelslike = weather["current"]["feels_like"]
        print("Feels-Like Temperature: " + str(feelslike) + chr(176) + "F/" + str(round((feelslike - 32)*5/9, 2)) + chr(176) + "C") #prints feels-like temperature in Farenheit and Celcius
        mainconditions = weather["current"]["weather"][0]["main"]
        descriptionconditions = weather["current"]["weather"][0]["description"]
        print("Conditions: " + mainconditions+ ", " + descriptionconditions) #prints current weather conditions and description
        windspeed = weather["current"]["wind_speed"]
        winddir = weather["current"]["wind_deg"]
        directions = ['North', 'Northeast', 'East', 'Southeast', 'South', 'Southwest', 'West', 'Northwest']
        directions_index = round(winddir / 45) % 8 #converts wind degrees to cardinal direction
        print("Wind: " + str(windspeed) + "mph " + directions[directions_index] ) #prints current wind speed and direction
        print("\n")
    return


def search_city(city, coords): 
    """Searches for the weather details of a given city and prints them.

    Args:
        city (str): The name of the city.
        coords (dict): City/Coordinate pairs
    """
    print_weather(city, coords)
    return

def add_city(city, favs): 
    """Adds a city to the user's favorites list.

    Args:
        city (str): The name of the city to add.
        favs (list): The list of favorite cities.

    Returns:
        bool: True if the city was added successfully, False otherwise.
    """
    if city.strip().title() in favs:
        print(f"{city} already in Favorites")
        return False
    elif len(favs) >= 3:
        print("Favorites List Full. Remove a city to add another.")
        return False
    elif not get_latlon(city):
        return False
    else:
        favs.append(city.title())
        print(f"{city} successfully added to favorites")
    return True

def list_favs(favs): 
    """Lists all favorite cities and displays their weather details.

    Args:
        favs (list): The list of favorite cities.
    """
    if len(favs) == 0:
        print("Favorites List Empty")
    else:
        print("Favorites List:\n")
        for city in favs:
            if(len(city) != 0):
                print_weather(city.strip())
    return

def remove_city(city, favs):
    """Removes a city from the user's favorites list.

    Args:
        city (str): The name of the city to remove.
        favs (list): The list of favorite cities.

    Returns:
        bool: True if the city was removed successfully, False otherwise.
    """
    
    if city not in favs:
        print(f"{city} not found in Favorites")
        return False
    else:
        favs.remove(city)
        print(f"{city} successfuly removed from Favorites")
    return True

def update_city(city_a, city_b, favs): 
    """Removes a city from the user's favorites list.

    Args:
        city (str): The name of the city to remove.
        favs (list): The list of favorite cities.

    Returns:
        bool: True if the city was removed successfully, False otherwise.
    """
    if remove_city(city_a, favs):
        if add_city(city_b, favs):
            return True
        else:
            add_city(city_a, favs)
    return False

def clear_favs(favs):
    """Clears all cities from the user's favorites list.

    Args:
        favs (list): The list of favorite cities.
    """
    if len(favs) == 0:
        print("Favorites list is already empty")
    else:
        favs.clear()
        print("Favorites list cleared")
    return
def main():
    """Runs the main weather application loop."""

    favs = []
    coords = {}
    firstRun = True 
    while(True):
        parser = create_parser()
        if firstRun: #Prints help message on first iteration
            parser.print_help()
            firstRun = False
        user_input = input("\nEnter command: ")
        
        
        try:
            args = parser.parse_args(shlex.split(user_input)) # Split the user input while preserving quotes
        except SystemExit:
            continue  # Prevent `-h` from exiting the program
        

        if args.help:
            parser.print_help()
        elif args.search:
            search_city(args.search, coords)
        elif args.add:
            add_city(args.add, favs)
        elif args.list:
            list_favs(favs)
        elif args.remove:
            remove_city(args.remove, favs)
        elif args.update:
            update_city(args.update[0], args.update[1], favs)
        elif args.clear:
            clear_favs(favs)
        elif args.exit:
            print("Exiting the Weather Application")
            break
        else:
            print("That is not a valid command")
            parser.print_help()

if __name__ == "__main__":
    main()
