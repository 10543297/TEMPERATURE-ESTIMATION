from bleak import BleakClient

MAC_ADDRESS = "5B:4B:3E:B4:DD:8F"

async def list_services():
    async with BleakClient(MAC_ADDRESS) as client:
        print("Connesso! Elenco servizi e caratteristiche:\n")
        for service in client.services:
            print(f"[SERVICE] {service.uuid} : {service.description}")
            for char in service.characteristics:
                print(f"  [CHAR] {char.uuid} : {char.properties}")

import asyncio
asyncio.run(list_services())
