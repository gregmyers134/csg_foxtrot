import requests
from datetime import datetime, timedelta

def fetch_baro_data(json_data):

    #print("BARO JSON: ",json_data)

        # Create a constructor class
    class BaroSensor:
        def __init__(self, uuid, created_at_str, created_at_datetime, altitude, serial_number,recorded_at_datetime):
            self.uuid = uuid
            self.created_at_str = created_at_str
            self.created_at_datetime = created_at_datetime
            self.altitude = altitude
            self.serial_number = serial_number
            self.recorded_at_datetime = recorded_at_datetime
            #self.sensor_key = sensor_key_value

    # Initialize an empty list to store instances of BaroSensor
    baro_objects = []

    # Iterate through the JSON data and filter based on the "sensor_key" field
    for obj_data in json_data:
        if "sensor" in obj_data and "sensor_key" in obj_data["sensor"]:
            sensor_key = obj_data["sensor"]["sensor_key"]
            if "BaroAltitude" in sensor_key:
                # Convert the created_at field to both datetime and string formats
                created_at_datetime = datetime.fromisoformat(obj_data["created_at"])
                created_at_str = obj_data["created_at"]
                altitude = obj_data["value"]
                recorded_at_datetime = datetime.fromisoformat(obj_data["recorded_at"])
                # Create an instance of LocationSensor with both created_at formats
                obj_instance = BaroSensor(
                    obj_data["uuid"],
                    created_at_str,
                    created_at_datetime,
                    altitude,
                    obj_data["serial_number"],
                    recorded_at_datetime
                )
                baro_objects.append(obj_instance)



    # Find the class object with the most recent created_at time (datetime format)
        sensor_key_value = "BaroAltitude"
        if any(obj_data.get("sensor", {}).get("sensor_key") == sensor_key_value for obj_data in json_data) and len(baro_objects) > 0:

            print("NUMBER OF BARO OBJECTS",len(baro_objects))
            most_recent_obj_datetime_baro = max(baro_objects, key=lambda obj: obj.recorded_at_datetime)

        # Find the class object with the most recent created_at time (string format)
            most_recent_obj_str = max(baro_objects, key=lambda obj: obj.created_at_str)

            
            formatted_string = f"UUID: {most_recent_obj_datetime_baro.uuid}, Altitude: {most_recent_obj_datetime_baro.altitude}, Time: {most_recent_obj_datetime_baro.created_at_str}"
            #print("Most recent recorded datetime:", most_recent_obj_datetime_baro.recorded_at_datetime)
           # print("Most recent created datetime:", most_recent_obj_datetime_baro.created_at_datetime)
            #print("Most recent string:", most_recent_obj_str.created_at_str)
            #print("STRING : ",formatted_string)

            return baro_objects
    
    else:
        print("no BARO DATA in RANGE")

    # Now, you can use these objects to access both datetime and string representations of created_at
    # You can also use the values from most_recent_obj_datetime or most_recent_obj_str to populate variables in a string
