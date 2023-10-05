import aiohttp
import asyncio

async def find_most_recent_baro(baro_objects):
    if not baro_objects:
        print("No baro_objects found.")
        return None

    most_recent_baro = None
    for baro_obj in baro_objects:
        if not isinstance(baro_obj, dict):
            print(f"Skipping invalid baro_obj of type {type(baro_obj)}")
            continue

        # Your logic for finding the most recent baro goes here.
        # For example, you might update most_recent_baro based on some condition.

    return most_recent_baro

async def location_data():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://localhost:8080/location') as resp:
            location_objects = await resp.json()

    if location_objects:
        for location_obj in location_objects:
            latitude = location_obj.get('latitude')
            longitude = location_obj.get('longitude')
            # ... (rest of your code)
    else:
        print("No location_objects found.")

    async with aiohttp.ClientSession() as session:
        async with session.get('http://localhost:8080/baro') as resp:
            baro_objects = await resp.json()

    most_recent_baro = await find_most_recent_baro(baro_objects)
    if most_recent_baro:
        # Do something with most_recent_baro
        pass
    else:
        print("No valid most_recent_baro found.")

async def main_loop():
    while True:
        await location_data()
        await asyncio.sleep(1)

if __name__ == "__main__":
    try:
        asyncio.run(main_loop())
    except Exception as e:
        print(f"An error occurred: {e}")