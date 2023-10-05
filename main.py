import asyncio
import aiohttp
from location_data import fetch_location_data
from baro_data import fetch_baro_data
from datetime import datetime, timedelta

def find_most_recent_location(location_objects):
    most_recent_locations = {}
    for location_obj in location_objects:
        serial_number = location_obj.serial_number
        if serial_number in most_recent_locations:
            if location_obj.recorded_at_datetime > most_recent_locations[serial_number].recorded_at_datetime:
                most_recent_locations[serial_number] = location_obj
        else:
            most_recent_locations[serial_number] = location_obj
    return most_recent_locations

def find_most_recent_baro(baro_objects):
    most_recent_baro = None
    serial_number = None
    recorded_at = None

    for baro_obj in baro_objects:
        if isinstance(baro_obj, dict):
            if 'serial_number' in baro_obj and 'recorded_at' in baro_obj:
                current_serial = baro_obj['serial_number']
                current_recorded_at = baro_obj['recorded_at']
                current_baro = baro_obj.get('value', None)

                if recorded_at is None or current_recorded_at > recorded_at:
                    recorded_at = current_recorded_at
                    serial_number = current_serial
                    most_recent_baro = current_baro

        elif isinstance(baro_obj, int):
            if most_recent_baro is None or baro_obj > most_recent_baro:
                most_recent_baro = baro_obj
                serial_number = "Default_Serial"
                recorded_at = "Default_Time"

    return serial_number, recorded_at, most_recent_baro

async def main():
    current_time = datetime.utcnow() 
    start_datetime_default = current_time - timedelta(seconds=10)
    end_datetime_default = current_time + timedelta(seconds=10)
    api_secret = "e7affe51ac1e4173b69cc815812ed6df"
    datetime_type = "recorded"

    start_datetime_default_iso = start_datetime_default.isoformat() + "Z"
    end_datetime_default_iso = end_datetime_default.isoformat() + "Z"

    request_url = "https://echotech.flightinsight.io/api/devices"

    payload = {
        'start_datetime': start_datetime_default_iso,
        'end_datetime': end_datetime_default_iso,
        'api_secret': api_secret,
        'datetime_type': datetime_type
    }
    headers = {}

    response = requests.request("POST", request_url, headers=headers, data=payload)

    if response.status_code == 200:
        response_data = response.json()
        json_data = response_data.get("data", {}).get("data", [])
        location_objects = fetch_location_data(json_data)
        baro_objects = fetch_baro_data(json_data)

    location_objects = await fetch_location_data(json_data)
    baro_objects = await fetch_baro_data(json_data)




    if baro_objectasync def is not None:
        serial_number, recorded_at, most_recent_baro = find_most_recent_baro(baro_objects)
        print(f"Serial Number: {serial_number}")
        print(f"Most Recent Recorded At: {recorded_at}")
        print(f"Altitude: {most_recent_baro}")
        print()
    else:
        print("MAIN: No BARO DATA in Time Range")

if __name__ == "__main__":
    asyncio.run(main())
