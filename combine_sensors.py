from location_data import fetch_location_data
from baro_data import fetch_baro_data
import requests
from datetime import datetime, timedelta


def find_most_recent_location(location_objects):
    # Create a dictionary to store the most recent location object for each serial number
    most_recent_locations = {}

    # Iterate through the location_objects list
    for location_obj in location_objects:
        serial_number = location_obj.serial_number

        # Check if the serial_number is already in the dictionary
        if serial_number in most_recent_locations:
            # Compare the recorded_at_datetime to find the most recent object
            if location_obj.recorded_at_datetime > most_recent_locations[serial_number].recorded_at_datetime:
                most_recent_locations[serial_number] = location_obj
        else:
            most_recent_locations[serial_number] = location_obj

    return most_recent_locations

def find_most_recent_baro(baro_objects):
    # Create a dictionary to store the most recent location object for each serial number
    most_recent_baro = {}

    # Iterate through the location_objects list
    for baro_obj in baro_objects:
        serial_number = baro_obj.serial_number

        # Check if the serial_number is already in the dictionary
        if serial_number in most_recent_baro:
            # Compare the recorded_at_datetime to find the most recent object
            if baro_obj.recorded_at_datetime > most_recent_baro[serial_number].recorded_at_datetime:
                most_recent_baro[serial_number] = baro_obj
        else:
            most_recent_baro[serial_number] = baro_obj

    return most_recent_baro

class Device:
    def __init__(self, serial_number):
        self.serial_number = serial_number
        self.latitude = 0  # Default value
        self.longitude = 0  # Default value
        self.altitude = 0  # Default value
        self.recorded_at_location = None
        self.recorded_at_baro = None
        self.location_updated = False  # Flag to track if location fields have been updated
        self.altitude_updated = False  # Flag to track if altitude field has been updated

    def update_location(self, latitude, longitude, recorded_at_location):
        # Update location fields only if they haven't been updated before
        if not self.location_updated:
            self.latitude = latitude
            self.longitude = longitude
            self.recorded_at_location = recorded_at_location
            self.location_updated = True

    def update_altitude(self, altitude, recorded_at_baro):
        # Update altitude field only if it hasn't been updated before
        if not self.altitude_updated:
            self.altitude = altitude
            self.recorded_at_baro = recorded_at_baro
            self.altitude_updated = True


if __name__ == "__main__":
    current_time = datetime.utcnow() 
    start_datetime_default = current_time - timedelta(seconds=10)
    end_datetime_default = current_time + timedelta(seconds=10)
    api_secret = "e7affe51ac1e4173b69cc815812ed6df"
    datetime_type = "recorded"

    start_datetime_default_iso = start_datetime_default.isoformat() + "Z"
    end_datetime_default_iso = end_datetime_default.isoformat() + "Z"

    request_url = "https://echotech.flightinsight.io/api/devices"




    # Construct the payload


    payload = {
        'start_datetime' : start_datetime_default_iso,
        'end_datetime' : end_datetime_default_iso,
        'api_secret' : api_secret,
        'datetime_type' : datetime_type
    }
    headers = {}

    response = requests.request("POST", request_url, headers=headers, data=payload)

    print(response.text)
    print(start_datetime_default_iso)

    



    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response into a Python object (list of dictionaries in this example)
        response_data = response.json()

        print("RESPONSE MAIN",response_data)

        json_data = response_data.get("data", {}).get("data", [])

        print("FIRST OBJECT",json_data[0])

        # Call the fetch_location_data function to get location_objects
        location_objects = fetch_location_data(json_data)
        
        baro_objects = fetch_baro_data(json_data)

        

        if location_objects is not None:
            # Find the most recent location objects for each serial number
            most_recent_locations = find_most_recent_location(location_objects)
            
            
            

            # Print the most recent location objects for each serial number
            for serial_number, location_obj in most_recent_locations.items():
                print(f"Serial Number: {serial_number}")
                print(f"Most Recent Recorded At: {location_obj.recorded_at_datetime}")
                print(f"Latitude: {location_obj.latitude}")
                print(f"Longitude: {location_obj.longitude}")
                print()

                
            
        else:
            print("MAIN: No LOCATION DATA in Time Range")


        if baro_objects is not None:
            # Find the most recent location objects for each serial number
            most_recent_baro = find_most_recent_baro(baro_objects)

            # Print the most recent location objects for each serial number
            for serial_number, baro_obj in most_recent_baro.items():
                print(f"Serial Number: {serial_number}")
                print(f"Most Recent Recorded At: {baro_obj.recorded_at_datetime}")
                print(f"Altitude: {baro_obj.altitude}")
                print()
                
        else:
            print("MAIN: No BARO DATA in Time Range")

            # Create a dictionary to store Device objects with serial numbers as keys
    devices = {}

    # Iterate through serial numbers
    serial_numbers = set(list(most_recent_locations.keys()) + list(most_recent_baro.keys()))
    for serial_number in serial_numbers:
        # Get most recent location and baro data for this serial number
        location_obj = most_recent_locations.get(serial_number)
        baro_obj = most_recent_baro.get(serial_number)

        # Create a Device object
        device = Device(
            serial_number=serial_number,
            latitude=location_obj.latitude if location_obj else None,
            longitude=location_obj.longitude if location_obj else None,
            recorded_at_location=location_obj.recorded_at_datetime if location_obj else None,
            altitude=baro_obj.altitude if baro_obj else None,
            recorded_at_baro=baro_obj.recorded_at_datetime if baro_obj else None,
        )

    for serial_number in serial_numbers:
        # Get most recent location and baro data for this serial number
        location_obj = most_recent_locations.get(serial_number)
        baro_obj = most_recent_baro.get(serial_number)

        # Create a Device object or retrieve an existing one
        if serial_number not in devices:
            device = Device(serial_number)
        else:
            device = devices[serial_number]

        # Update location and altitude if data is available
        if location_obj:
            device.update_location(location_obj.latitude, location_obj.longitude, location_obj.recorded_at_location)
        if baro_obj:
            device.update_altitude(baro_obj.altitude, baro_obj.recorded_at_baro)

            # Store the Device object in the devices dictionary
            devices[serial_number] = device

        # Print all Device objects
    for serial_number, device in devices.items():
        print(f"Serial Number: {device.serial_number}")
        print(f"Latitude: {device.latitude}")
        print(f"Longitude: {device.longitude}")
        print(f"Recorded At Location: {device.recorded_at_location}")
        print(f"Altitude: {device.altitude}")
        print(f"Recorded At Baro: {device.recorded_at_baro}")
        print()