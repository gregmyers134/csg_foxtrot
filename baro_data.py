# Initialize a variable to store the last received altitude value
last_received_altitude = 0

async def fetch_baro_data(json_data):
    global last_received_altitude  # Declare the variable as global to modify it

    baro_objects = []

    if not json_data:
        print("Warning: Received empty JSON data.")
        return [last_received_altitude]  # Return the last received value as a list

    baro_data_found = False

    for obj_data in json_data:
        if "sensor" in obj_data and "sensor_key" in obj_data["sensor"]:
            sensor_key = obj_data["sensor"]["sensor_key"]
            if "BaroAltitude" in sensor_key:
                baro_data_found = True
                altitude = float(obj_data["value"])  # Assuming the altitude is stored in "value" key
                last_received_altitude = altitude  # Update the last received value
                baro_objects.append(obj_data)  # Add to baro_objects list

    if not baro_data_found:
        print(f"Warning: No BaroAltitude data found in the provided JSON. Using last received value: {last_received_altitude}")
        return [last_received_altitude]  # Return the last received value as a list

    return baro_objects  # Return the list of baro objects
