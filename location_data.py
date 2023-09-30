import requests, json
from datetime import datetime, timedelta

def fetch_location_data(json_data):

    jsonDic = json_data

    # Create a constructor class
    class LocationSensor:
        def __init__(self, uuid, created_at_str, created_at_datetime, latitude, longitude, serial_number,recorded_at_datetime):
            self.uuid = uuid
            self.created_at_str = created_at_str
            self.created_at_datetime = created_at_datetime
            self.latitude = latitude
            self.longitude = longitude
            self.serial_number = serial_number
            self.recorded_at_datetime = recorded_at_datetime
            #self.sensor_key = sensor_key_value

    # Initialize an empty list to store instances of LocationSensor
    location_objects = []

    # Iterate through the JSON data and filter based on the "sensor_key" field
    for obj_data in jsonDic:
        if "sensor" in obj_data and "sensor_key" in obj_data["sensor"]:
            sensor_key = obj_data["sensor"]["sensor_key"]
            if "vb_location" in sensor_key:
                # Extract latitude and longitude
                ###latitude, longitude = float(obj_data["value"][0]), float(obj_data["value"][1])
                latitude, longitude = float(obj_data["geolocation"]["coordinates"][0]), float(obj_data["geolocation"]["coordinates"][1])
                # Convert the created_at field to both datetime and string formats
                created_at_datetime = datetime.fromisoformat(obj_data["created_at"])
                created_at_str = obj_data["created_at"]
                recorded_at_datetime = datetime.fromisoformat(obj_data["recorded_at"])
                # Create an instance of LocationSensor with both created_at formats
                obj_instance = LocationSensor(
                    obj_data["uuid"],
                    created_at_str,
                    created_at_datetime,
                    latitude,
                    longitude,
                    obj_data["serial_number"],
                    recorded_at_datetime
                )
                location_objects.append(obj_instance)


   # Check if "vb_location" sensor key is found in the JSON data
        sensor_key_value = "vb_location"
        if any(obj_data.get("sensor", {}).get("sensor_key") == sensor_key_value for obj_data in jsonDic)and len(location_objects) > 0:
            
            
            print(f"'{sensor_key_value}' is found in the JSON data.")


            print("NUMBER OF LOCATION OBJECTS",len(location_objects))
            most_recent_obj_datetime = max(location_objects, key=lambda obj: obj.recorded_at_datetime)

        # Find the class object with the most recent created_at time (string format)
            most_recent_obj_str = max(location_objects, key=lambda obj: obj.created_at_str)

            
            #formatted_string = f"UUID: {most_recent_obj_datetime.uuid}, Latitude: {most_recent_obj_datetime.latitude}, Longitude: {most_recent_obj_datetime.longitude}, Time: {most_recent_obj_datetime.created_at_str}"
            #print("Most recent recorded datetime:", most_recent_obj_datetime.recorded_at_datetime)
            #print("Most recent created datetime:", most_recent_obj_datetime.created_at_datetime)
            #print("Most recent string:", most_recent_obj_str.created_at_str)
            #print("STRING : ",formatted_string)

            return location_objects
            
        else:
            print("no LOCATION DATA in RANGE")

    else:
            print(f"'{sensor_key_value}' is not found in the JSON data.")

    # Now, you can use these objects to access both datetime and string representations of created_at
    # You can also use the values from most_recent_obj_datetime or most_recent_obj_str to populate variables in a string

