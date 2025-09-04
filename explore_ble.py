import asyncio
from bleak import BleakClient

ADDRESS = "E3:5D:4F:FA:E3:F8"  # Indirizzo del tuo SteadyTemp

async def explore(address):
    async with BleakClient(address) as client:
        print(f"🔗 Connesso a {address}")
        services = await client.get_services()
        for service in services:
            print(f"\n🛠 Servizio: {service.uuid}")
            for char in service.characteristics:
                print(f"  ↳ Caratteristica: {char.uuid}")
                print(f"     • Properties: {char.properties}")

asyncio.run(explore(ADDRESS))
