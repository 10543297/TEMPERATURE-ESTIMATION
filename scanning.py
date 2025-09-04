import asyncio
from bleak import BleakScanner

async def scan():
    print("🔍 Scanning BLE devices per 15 secondi...")
    devices = await BleakScanner.discover(timeout=15.0)
    for d in devices:
        print(f"{d.name} - {d.address} - RSSI: {d.rssi}")

asyncio.run(scan())
