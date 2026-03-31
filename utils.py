import aiohttp, os

async def get_uuid(username: str) -> str | None:
    try:
        async with aiohttp.request("GET", f"https://api.mojang.com/users/profiles/minecraft/{username}") as response:
            data = await response.json()
            return data.get('id')
    except Exception as e:
        print(f'Error fetching uuid: {e}')
        return None

import datetime
from zoneinfo import ZoneInfo
async def notify(uuid: str, username: str) -> None:
    import main
    try:
        async with aiohttp.request("GET", f"https://api.hypixel.net/guild?key={os.getenv('HYPIXEL_API_KEY')}&player={uuid}") as response:
            data = await response.json()
            if 'guild' not in data: return
            guild = data['guild']
            member = [m for m in guild['members'] if m['uuid'] == uuid][0]
            expHistory = member['expHistory']

            current_date = datetime.datetime.now().astimezone(ZoneInfo('America/New_York'))
            year = current_date.year
            month = str(current_date.month).rjust(2, '0')
            day = str(current_date.day).rjust(2, '0')
            key = f'{year}-{month}-{day}'
            if main.last_gexp[uuid] != -1 and main.last_gexp[uuid] != expHistory[key]:
                await main.AIDAN.send(f':rotating_light: User {username} has had changes in their guild experience :rotating_light:')
            main.last_gexp[uuid] = expHistory[key]
    except Exception as e:
        print(f'Something went wrong: {e}')