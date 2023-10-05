import asyncio
import aiohttp
from location_data import fetch_location_data
from baro_data import fetch_baro_data
import requests
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
    most_recent_baro = {}
    for baro_obj in baro_objects:
        serial_number = baro_obj.serial_number
        if serial_number in most_recent_baro:
            if baro_obj.recorded_at_datetime > most_recent_baro[serial_number].recorded_at_datetime:
                most_recent_baro[serial_number] = baro_obj
        else:
            most_recent_baro[serial_number] = baro_obj
    return most_recent_baro


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

    # Making the request asynchronous
    async with aiohttp.ClientSession() as session:
        async with session.post(request_url, headers=headers, json=payload) as response:
            if response.status == 200:
                response_data = await response.json()
                json_data = response_data.get("data", {}).get("data", [])
                
                # Assuming fetch_location_data and fetch_baro_data are asynchronous
                location_objects = await fetch_location_data(json_data)
                baro_objects = await fetch_baro_data(json_data)

                if location_objects is not None:
                    most_recent_locations = find_most_recent_location(location_objects)
                    for serial_number, location_obj in most_recent_locations.items():
                        print(f"Serial Number: {serial_number}")
                        print(f"Most Recent Recorded At: {location_obj.recorded_at_datetime}")
                        print(f"Latitude: {location_obj.latitude}")
                        print(f"Longitude: {location_obj.longitude}")
                        print()
                else:
                    print("MAIN: No LOCATION DATA in Time Range")

                if baro_objects is not None:
                    most_recent_baro = find_most_recent_baro(baro_objects)
                    for serial_number, baro_obj in most_recent_baro.items():
                        print(f"Serial Number: {serial_number}")
                        print(f"Most Recent Recorded At: {baro_obj.recorded_at_datetime}")
                        print(f"Altitude: {baro_obj.altitude}")
                        print()
                else:
                    print("MAIN: No BARO DATA in Time Range")

if __name__ == "__main__":
    asyncio.run(main())